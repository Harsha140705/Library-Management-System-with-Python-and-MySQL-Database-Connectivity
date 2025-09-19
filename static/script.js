// Custom JavaScript for The Book Worm Library Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Animated Counter for Stats
    function animateCounters() {
        var counters = document.querySelectorAll('.stat-number');
        counters.forEach(function(counter) {
            var target = parseFloat(counter.getAttribute('data-count'));
            var current = 0;
            var increment = target / 100;
            var timer = setInterval(function() {
                current += increment;
                if (current >= target) {
                    counter.textContent = target % 1 === 0 ? target : target.toFixed(1);
                    clearInterval(timer);
                } else {
                    counter.textContent = current % 1 === 0 ? Math.floor(current) : current.toFixed(1);
                }
            }, 20);
        });
    }

    // Intersection Observer for animations
    var observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Trigger counter animation for stats section
                if (entry.target.classList.contains('stats-section')) {
                    animateCounters();
                }
            }
        });
    }, observerOptions);

    // Observe elements for animation
    var animateElements = document.querySelectorAll('.feature-card, .access-card, .stat-card, .stats-section');
    animateElements.forEach(function(el) {
        observer.observe(el);
    });

    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        var scrolled = window.pageYOffset;
        var heroBackground = document.querySelector('.hero-background');
        if (heroBackground) {
            heroBackground.style.transform = 'translateY(' + (scrolled * 0.5) + 'px)';
        }
    });

    // Enhanced button interactions
    var heroButtons = document.querySelectorAll('.btn-hero');
    heroButtons.forEach(function(button) {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Card hover effects with 3D transform
    var cards = document.querySelectorAll('.access-card, .feature-card');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) rotateX(5deg)';
            this.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotateX(0deg)';
            this.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        });
    });

    // Floating books animation enhancement
    var books = document.querySelectorAll('.book');
    books.forEach(function(book, index) {
        book.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-30px) rotate(10deg) scale(1.2)';
            this.style.transition = 'all 0.3s ease';
        });
        
        book.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotate(0deg) scale(1)';
        });
    });

    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Typing effect for hero title
    function typeWriter(element, text, speed = 100) {
        var i = 0;
        element.innerHTML = '';
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        type();
    }

    // Add typing effect to hero title if it exists
    var heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        var originalText = heroTitle.textContent;
        setTimeout(function() {
            typeWriter(heroTitle, originalText, 50);
        }, 1000);
    }

    // Particle effect for hero section
    function createParticles() {
        var heroSection = document.querySelector('.hero-section-enhanced');
        if (!heroSection) return;
        
        for (var i = 0; i < 20; i++) {
            var particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float ${3 + Math.random() * 4}s ease-in-out infinite;
                animation-delay: ${Math.random() * 2}s;
            `;
            heroSection.appendChild(particle);
        }
    }

    createParticles();

    // Add CSS for particles
    var style = document.createElement('style');
    style.textContent = `
        .particle {
            pointer-events: none;
        }
        .animate-in {
            animation: slideInUp 0.6s ease-out forwards;
        }
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);

    // Add loading state to forms
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                var originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                submitBtn.disabled = true;
                
                // Re-enable button after 3 seconds (fallback)
                setTimeout(function() {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });

    // Add fade-in animation to cards
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(function() {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Add hover effects to table rows
    var tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(0, 123, 255, 0.05)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Search functionality for tables
    var searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(function(input) {
        input.addEventListener('keyup', function() {
            var filter = this.value.toLowerCase();
            var table = this.closest('.card').querySelector('table');
            var rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                if (text.indexOf(filter) > -1) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Rating display enhancement
    var ratingDisplays = document.querySelectorAll('.rating-display');
    ratingDisplays.forEach(function(display) {
        var rating = parseInt(display.querySelector('.badge').textContent);
        var stars = display.querySelectorAll('.stars i');
        
        stars.forEach(function(star, index) {
            if (index < rating) {
                star.classList.add('fas', 'fa-star');
                star.classList.remove('far');
            } else {
                star.classList.add('far');
                star.classList.remove('fas');
            }
        });
    });

    // Confirmation dialogs
    var deleteButtons = document.querySelectorAll('[onclick*="confirm"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to perform this action?')) {
                e.preventDefault();
            }
        });
    });

    // Form validation enhancement
    var requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredFields.forEach(function(field) {
        field.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });

    // Password strength indicator
    var passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(function(field) {
        field.addEventListener('input', function() {
            var password = this.value;
            var strength = 0;
            
            if (password.length >= 6) strength++;
            if (password.match(/[a-z]/)) strength++;
            if (password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;
            
            var strengthIndicator = this.parentNode.querySelector('.password-strength');
            if (strengthIndicator) {
                strengthIndicator.className = 'password-strength strength-' + strength;
            }
        });
    });

    // Book card hover effects
    var bookCards = document.querySelectorAll('.card.h-100');
    bookCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        });
    });

    // Statistics counter animation
    var counters = document.querySelectorAll('.card-body h3');
    counters.forEach(function(counter) {
        var target = parseInt(counter.textContent);
        var current = 0;
        var increment = target / 50;
        
        var timer = setInterval(function() {
            current += increment;
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current);
            }
        }, 30);
    });

    // Mobile menu enhancement
    var navbarToggler = document.querySelector('.navbar-toggler');
    var navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }

    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-resize textareas
    var textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Print functionality
    var printButtons = document.querySelectorAll('.print-btn');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Dark mode toggle (if implemented)
    var darkModeToggle = document.querySelector('#darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
        
        // Load saved dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }
});

// Utility functions
function showNotification(message, type = 'info') {
    var alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function debounce(func, wait) {
    var timeout;
    return function executedFunction(...args) {
        var later = function() {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global use
window.LibraryUtils = {
    showNotification: showNotification,
    formatDate: formatDate,
    debounce: debounce
};
