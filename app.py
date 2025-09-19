from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from functools import wraps
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
DB_CONFIG = {
    'host': 'dpg-d36q062li9vc73dbugcg-a',
    'user': 'thebookworm_user',
    'password': '6fb5ZGBG0bXoZzRKLW6cCQihLQHG9cim',
    'database': 'thebookworm'
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def init_database():
    """Initialize database tables if they don't exist"""
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Create BookRecord table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BookRecord (
                BookID varchar(10) PRIMARY KEY,
                BookName varchar(35),
                Author varchar(30),
                Publisher varchar(30)
            )
        """)
        
        # Create UserRecord table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserRecord (
                UserID varchar(10) PRIMARY KEY,
                UserName varchar(20),
                Password varchar(20),
                BookID varchar(10),
                FOREIGN KEY (BookID) REFERENCES BookRecord(BookID)
            )
        """)
        
        # Create AdminRecord table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AdminRecord (
                AdminID varchar(10) PRIMARY KEY,
                Password varchar(20)
            )
        """)
        
        # Create Feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Feedback (
                Feedback varchar(100) PRIMARY KEY,
                Rating varchar(10)
            )
        """)
        
        # Insert default data if tables are empty
        cursor.execute("SELECT COUNT(*) FROM UserRecord")
        if cursor.fetchone()[0] == 0:
            default_users = [
                ("101", "Kunal", "1234", None),
                ("102", "Vishal", "3050", None),
                ("103", "Siddhesh", "5010", None)
            ]
            cursor.executemany("INSERT INTO UserRecord VALUES (%s, %s, %s, %s)", default_users)
        
        cursor.execute("SELECT COUNT(*) FROM AdminRecord")
        if cursor.fetchone()[0] == 0:
            default_admins = [
                ("Kunal1020", "123"),
                ("Siddesh510", "786"),
                ("Vishal305", "675")
            ]
            cursor.executemany("INSERT INTO AdminRecord VALUES (%s, %s)", default_admins)
        
        connection.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and 'admin_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        
        connection = get_db_connection()
        if not connection:
            flash('Database connection error.', 'error')
            return render_template('login.html')
        
        cursor = connection.cursor()
        
        try:
            if user_type == 'admin':
                cursor.execute("SELECT AdminID FROM AdminRecord WHERE AdminID = %s AND Password = %s", 
                             (user_id, password))
                result = cursor.fetchone()
                if result:
                    session['admin_id'] = user_id
                    flash(f'Welcome, {user_id}!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid admin credentials.', 'error')
            else:
                cursor.execute("SELECT UserID, UserName FROM UserRecord WHERE UserID = %s AND Password = %s", 
                             (user_id, password))
                result = cursor.fetchone()
                if result:
                    session['user_id'] = user_id
                    session['user_name'] = result[1]
                    flash(f'Welcome, {result[1]}!', 'success')
                    return redirect(url_for('user_dashboard'))
                else:
                    flash('Invalid user credentials.', 'error')
        
        except mysql.connector.Error as err:
            flash('Database error occurred.', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        
        connection = get_db_connection()
        if not connection:
            flash('Database connection error.', 'error')
            return render_template('register.html')
        
        cursor = connection.cursor()
        
        try:
            # Check if user already exists
            cursor.execute("SELECT UserID FROM UserRecord WHERE UserID = %s", (user_id,))
            if cursor.fetchone():
                flash('User ID already exists.', 'error')
                return render_template('register.html')
            
            # Insert new user
            cursor.execute("INSERT INTO UserRecord (UserID, UserName, Password, BookID) VALUES (%s, %s, %s, %s)",
                         (user_id, user_name, password, None))
            connection.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        
        except mysql.connector.Error as err:
            flash('Database error occurred.', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('register.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return render_template('admin_dashboard.html', stats={})
    
    cursor = connection.cursor()
    try:
        # Get total books count
        cursor.execute("SELECT COUNT(*) FROM BookRecord")
        total_books = cursor.fetchone()[0]
        
        # Get total users count
        cursor.execute("SELECT COUNT(*) FROM UserRecord")
        total_users = cursor.fetchone()[0]
        
        # Get books currently issued
        cursor.execute("SELECT COUNT(*) FROM UserRecord WHERE BookID IS NOT NULL")
        books_issued = cursor.fetchone()[0]
        
        # Get total feedback count
        cursor.execute("SELECT COUNT(*) FROM Feedback")
        total_feedback = cursor.fetchone()[0]
        
        # Get recent activity (last 5 books added)
        cursor.execute("SELECT BookName, Author FROM BookRecord ORDER BY BookID DESC LIMIT 5")
        recent_books = cursor.fetchall()
        
        # Get recent users
        cursor.execute("SELECT UserName FROM UserRecord ORDER BY UserID DESC LIMIT 3")
        recent_users = cursor.fetchall()
        
        # Get recent feedback
        cursor.execute("SELECT Feedback, Rating FROM Feedback ORDER BY Feedback DESC LIMIT 3")
        recent_feedback = cursor.fetchall()
        
        stats = {
            'total_books': total_books,
            'total_users': total_users,
            'books_issued': books_issued,
            'total_feedback': total_feedback,
            'recent_books': recent_books,
            'recent_users': recent_users,
            'recent_feedback': recent_feedback
        }
        
    except mysql.connector.Error as err:
        flash('Database error occurred.', 'error')
        stats = {
            'total_books': 0,
            'total_users': 0,
            'books_issued': 0,
            'total_feedback': 0,
            'recent_books': [],
            'recent_users': [],
            'recent_feedback': []
        }
    finally:
        cursor.close()
        connection.close()
    
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    """User dashboard"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return render_template('user_dashboard.html', user_stats={})
    
    cursor = connection.cursor()
    try:
        # Get user's currently issued book
        cursor.execute("""
            SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher
            FROM BookRecord
            INNER JOIN UserRecord ON BookRecord.BookID = UserRecord.BookID
            WHERE UserRecord.UserID = %s
        """, (session['user_id'],))
        issued_book = cursor.fetchone()
        
        # Get total available books
        cursor.execute("""
            SELECT COUNT(*) FROM BookRecord
            LEFT JOIN UserRecord ON BookRecord.BookID = UserRecord.BookID
            WHERE UserRecord.BookID IS NULL
        """)
        available_books = cursor.fetchone()[0]
        
        # Get total books in library
        cursor.execute("SELECT COUNT(*) FROM BookRecord")
        total_books = cursor.fetchone()[0]
        
        user_stats = {
            'issued_book': issued_book,
            'available_books': available_books,
            'total_books': total_books,
            'has_book': issued_book is not None
        }
        
    except mysql.connector.Error as err:
        flash('Database error occurred.', 'error')
        user_stats = {
            'issued_book': None,
            'available_books': 0,
            'total_books': 0,
            'has_book': False
        }
    finally:
        cursor.close()
        connection.close()
    
    return render_template('user_dashboard.html', user_stats=user_stats)

@app.route('/admin/books')
@admin_required
def admin_books():
    """Admin book management"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, 
                   BookRecord.Publisher, UserRecord.UserName, UserRecord.UserID
            FROM BookRecord
            LEFT JOIN UserRecord ON BookRecord.BookID = UserRecord.BookID
            ORDER BY BookRecord.BookID
        """)
        books = cursor.fetchall()
    except mysql.connector.Error as err:
        flash('Database error occurred.', 'error')
        books = []
    finally:
        cursor.close()
        connection.close()
    
    return render_template('admin_books.html', books=books)

@app.route('/admin/books/add', methods=['POST'])
@admin_required
def add_book():
    """Add new book"""
    book_id = request.form.get('book_id')
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('admin_books'))
    
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO BookRecord (BookID, BookName, Author, Publisher) VALUES (%s, %s, %s, %s)",
                     (book_id, book_name, author, publisher))
        connection.commit()
        flash('Book added successfully!', 'success')
    except mysql.connector.Error as err:
        flash('Error adding book. Book ID might already exist.', 'error')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('admin_books'))

@app.route('/admin/books/delete/<book_id>')
@admin_required
def delete_book(book_id):
    """Delete book"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('admin_books'))
    
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM BookRecord WHERE BookID = %s", (book_id,))
        connection.commit()
        flash('Book deleted successfully!', 'success')
    except mysql.connector.Error as err:
        flash('Error deleting book.', 'error')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('admin_books'))

@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin user management"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT UserRecord.UserID, UserRecord.UserName, UserRecord.Password,
                   BookRecord.BookName, BookRecord.BookID
            FROM UserRecord
            LEFT JOIN BookRecord ON UserRecord.BookID = BookRecord.BookID
            ORDER BY UserRecord.UserID
        """)
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        flash('Database error occurred.', 'error')
        users = []
    finally:
        cursor.close()
        connection.close()
    
    return render_template('admin_users.html', users=users)

@app.route('/user/books')
@login_required
def user_books():
    """User book browsing"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('user_dashboard'))
    
    cursor = connection.cursor()
    try:
        # Get available books (not issued to anyone)
        cursor.execute("""
            SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher
            FROM BookRecord
            LEFT JOIN UserRecord ON BookRecord.BookID = UserRecord.BookID
            WHERE UserRecord.BookID IS NULL
            ORDER BY BookRecord.BookName
        """)
        available_books = cursor.fetchall()
        
        # Get user's currently issued book
        cursor.execute("""
            SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher
            FROM BookRecord
            INNER JOIN UserRecord ON BookRecord.BookID = UserRecord.BookID
            WHERE UserRecord.UserID = %s
        """, (session['user_id'],))
        issued_book = cursor.fetchone()
        
    except mysql.connector.Error as err:
        flash('Database error occurred.', 'error')
        available_books = []
        issued_book = None
    finally:
        cursor.close()
        connection.close()
    
    return render_template('user_books.html', available_books=available_books, issued_book=issued_book)

@app.route('/user/issue/<book_id>')
@login_required
def issue_book(book_id):
    """Issue book to user"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('user_books'))
    
    cursor = connection.cursor()
    try:
        # Check if user already has a book
        cursor.execute("SELECT BookID FROM UserRecord WHERE UserID = %s AND BookID IS NOT NULL", 
                     (session['user_id'],))
        if cursor.fetchone():
            flash('You already have a book issued. Please return it first.', 'error')
            return redirect(url_for('user_books'))
        
        # Issue the book
        cursor.execute("UPDATE UserRecord SET BookID = %s WHERE UserID = %s", 
                     (book_id, session['user_id']))
        connection.commit()
        flash('Book issued successfully!', 'success')
        
    except mysql.connector.Error as err:
        flash('Error issuing book.', 'error')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('user_books'))

@app.route('/user/return/<book_id>')
@login_required
def return_book(book_id):
    """Return book"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('user_books'))
    
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE UserRecord SET BookID = NULL WHERE UserID = %s AND BookID = %s", 
                     (session['user_id'], book_id))
        connection.commit()
        flash('Book returned successfully!', 'success')
        
    except mysql.connector.Error as err:
        flash('Error returning book.', 'error')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('user_books'))

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    """User feedback page"""
    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        rating = request.form.get('rating')
        
        connection = get_db_connection()
        if not connection:
            flash('Database connection error.', 'error')
            return render_template('feedback.html')
        
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Feedback (Feedback, Rating) VALUES (%s, %s)",
                         (feedback_text, rating))
            connection.commit()
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('user_dashboard'))
        
        except mysql.connector.Error as err:
            flash('Error submitting feedback.', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('feedback.html')

@app.route('/admin/feedback')
@admin_required
def admin_feedback():
    """Admin feedback view"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT Feedback, Rating FROM Feedback ORDER BY Feedback")
        feedbacks = cursor.fetchall()
    except mysql.connector.Error as err:
        flash('Database error occurred.', 'error')
        feedbacks = []
    finally:
        cursor.close()
        connection.close()
    
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize database
    if init_database():
        print("Database initialized successfully!")
    else:
        print("Database initialization failed!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
