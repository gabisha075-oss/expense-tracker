// =============================================
// GLOBAL FUNCTIONS & UTILITIES
// ============================================= */

// Smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Hamburger menu toggle
const hamburger = document.querySelector('.hamburger');
const navbarMenu = document.querySelector('.navbar-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navbarMenu.classList.toggle('active');
    });
}

// Close menu when a link is clicked
if (navbarMenu) {
    navbarMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navbarMenu.classList.remove('active');
        });
    });
}

// Auto-hide alert messages
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            alert.style.display = 'none';
        }, 300);
    }, 5000);
});

// =============================================
// FORM ENHANCEMENTS
// ============================================= */

// Amount input formatting
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('blur', function() {
        if (this.value) {
            this.value = parseFloat(this.value).toFixed(2);
        }
    });
});

// Date input - set today as default
window.addEventListener('load', () => {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            input.value = `${year}-${month}-${day}`;
        }
    });
});

// =============================================
// DASHBOARD INTERACTIONS
// ============================================= */

// Quick stats animation on load
function animateStats() {
    const stats = document.querySelectorAll('.card-amount');
    stats.forEach((stat, index) => {
        setTimeout(() => {
            stat.style.animation = 'pulse 0.6s ease-out';
        }, index * 100);
    });
}

// Transaction list hover effects
document.querySelectorAll('.transaction-item').forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(5px)';
    });
    item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0)';
    });
});

// =============================================
// CATEGORY MANAGEMENT
// ============================================= */

// Color picker preview
const colorInput = document.getElementById('color');
const colorPreview = document.getElementById('colorPreview');

if (colorInput && colorPreview) {
    colorInput.addEventListener('input', (e) => {
        colorPreview.style.backgroundColor = e.target.value;
    });
}

// =============================================
// BUDGET PAGE INTERACTIONS
// ============================================= */

// Budget card animations
document.querySelectorAll('.budget-card').forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
});

// Progress bar animation
function animateProgressBars() {
    document.querySelectorAll('.progress-fill').forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-out';
            bar.style.width = width;
        }, 100);
    });
}

if (document.querySelector('.budget-card')) {
    window.addEventListener('load', animateProgressBars);
}

// =============================================
// CHARTS INTERACTION
// ============================================= */

// Chart tooltip enhancements
if (typeof Chart !== 'undefined') {
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.color = '#7f8c8d';
}

// =============================================
// FORM VALIDATION
// ============================================= */

// Change password form
const changePasswordForm = document.getElementById('changePasswordForm');
if (changePasswordForm) {
    changePasswordForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        try {
            const response = await fetch('{% url "change_password" %}', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const result = await response.json();
            if (result.success) {
                alert(result.message);
                this.reset();
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred');
        }
    });
}

// =============================================
// UTILITY FUNCTIONS
// ============================================= */

// Format currency
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        const notification = document.createElement('div');
        notification.textContent = 'Copied to clipboard!';
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 1000;
            animation: slideUp 0.3s ease-out;
        `;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    });
}

// =============================================
// PAGE LOAD ANIMATIONS
// ============================================= */

// Stagger animations on page load
window.addEventListener('load', () => {
    const cardsToAnimate = document.querySelectorAll('[style*="animation"]');
    cardsToAnimate.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
});

// =============================================
// MOBILE OPTIMIZATIONS
// ============================================= */

// Touch-friendly interactions
if (window.innerWidth <= 768) {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.style.minHeight = '44px';
        btn.style.minWidth = '44px';
    });

    document.querySelectorAll('a').forEach(link => {
        const rect = link.getBoundingClientRect();
        if (rect.height < 44 || rect.width < 44) {
            link.style.padding = '12px 16px';
        }
    });
}

// =============================================
// LOCAL STORAGE HELPERS
// ============================================= */

// Save theme preference
const setTheme = (theme) => {
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
};

const getTheme = () => {
    return localStorage.getItem('theme') || 'light';
};

// =============================================
// ACCESSIBILITY
// ============================================= */

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    // Escape key to close dropdowns
    if (e.key === 'Escape') {
        document.querySelectorAll('.dropdown-menu.active').forEach(menu => {
            menu.classList.remove('active');
        });
    }
});

// Password visibility toggle
function initPasswordToggle() {
    const toggleButton = document.querySelector('.password-toggle');
    const passwordField = document.querySelector('#password');

    if (!toggleButton || !passwordField) {
        return;
    }

    toggleButton.addEventListener('click', () => {
        const isPassword = passwordField.type === 'password';
        passwordField.type = isPassword ? 'text' : 'password';
        const icon = toggleButton.querySelector('i');
        if (icon) {
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        }
    });
}

// =============================================
// INITIALIZATION
// ============================================= */

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize animations
    animateStats();
    initPasswordToggle();
    
    // Log initialization (for debugging)
    console.log('ExpenseTracker initialized successfully!');
});
