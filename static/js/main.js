// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId !== '#') {
            e.preventDefault();
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Installment plan selection
document.querySelectorAll('.installment-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.installment-card').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        const radio = this.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
        }
    });
});

// Star rating for reviews
document.querySelectorAll('.rating-input input[type="radio"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const value = this.value;
        const container = this.closest('.rating-input');
        container.querySelectorAll('label i').forEach((star, index) => {
            if (index < value) {
                star.classList.remove('far');
                star.classList.add('fas');
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
            }
        });
    });
});

// Auto-hide alerts after 5 seconds
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    }, 5000);
});

// Confirm delete actions
document.querySelectorAll('[data-confirm]').forEach(button => {
    button.addEventListener('click', function(e) {
        const message = this.getAttribute('data-confirm');
        if (!confirm(message)) {
            e.preventDefault();
        }
    });
});

// Image preview on file input
document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function() {
        const preview = this.nextElementSibling;
        if (preview && preview.classList.contains('image-preview')) {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }
    });
});

// Password visibility toggle
document.querySelectorAll('.password-toggle').forEach(button => {
    button.addEventListener('click', function() {
        const input = this.previousElementSibling;
        const icon = this.querySelector('i');
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });
});

// Copy to clipboard
document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', function() {
        const text = this.getAttribute('data-copy');
        navigator.clipboard.writeText(text).then(() => {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> Nusxa olindi';
            setTimeout(() => {
                this.innerHTML = originalText;
            }, 2000);
        });
    });
});

// Lazy load images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img.lazy').forEach(img => {
        imageObserver.observe(img);
    });
}

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('shadow');
    } else {
        navbar.classList.remove('shadow');
    }
});

// Form validation
document.querySelectorAll('form[data-validate]').forEach(form => {
    form.addEventListener('submit', function(e) {
        let isValid = true;
        form.querySelectorAll('[required]').forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('is-invalid');
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
        }
    });
});

// Search debounce
let searchTimeout;
document.querySelectorAll('[data-search]').forEach(input => {
    input.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = this.value;
            const url = this.getAttribute('data-search');
            if (query.length >= 2) {
                window.location.href = `${url}?q=${encodeURIComponent(query)}`;
            }
        }, 500);
    });
});

// Tab persistence
document.querySelectorAll('[data-tab-persist]').forEach(tab => {
    const tabId = tab.getAttribute('data-tab-persist');
    const savedTab = localStorage.getItem(`tab-${tabId}`);
    if (savedTab) {
        const tabButton = tab.querySelector(`[data-bs-target="#${savedTab}"]`);
        if (tabButton) {
            new bootstrap.Tab(tabButton).show();
        }
    }
    
    tab.querySelectorAll('[data-bs-toggle="tab"]').forEach(button => {
        button.addEventListener('shown.bs.tab', function(e) {
            const targetId = e.target.getAttribute('data-bs-target').substring(1);
            localStorage.setItem(`tab-${tabId}`, targetId);
        });
    });
});

// Dynamic year in footer
document.addEventListener('DOMContentLoaded', function() {
    const yearElements = document.querySelectorAll('[data-year]');
    const currentYear = new Date().getFullYear();
    yearElements.forEach(element => {
        element.textContent = currentYear;
    });
});

// Live search functionality
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
let liveSearchTimeout;

if (searchInput && searchResults) {
    searchInput.addEventListener('input', function() {
        clearTimeout(liveSearchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        liveSearchTimeout = setTimeout(() => {
            fetch(`/courses/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.results.length > 0) {
                        searchResults.innerHTML = data.results.map(course => `
                            <a href="/courses/${course.slug}/" class="text-decoration-none">
                                <div class="p-3 border-bottom hover-bg-light">
                                    <div class="d-flex gap-3">
                                        ${course.thumbnail ? 
                                            `<img src="${course.thumbnail}" alt="${course.title}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;">` :
                                            `<div class="bg-primary d-flex align-items-center justify-content-center" style="width: 50px; height: 50px; border-radius: 8px;">
                                                <i class="fas fa-graduation-cap text-white"></i>
                                            </div>`
                                        }
                                        <div class="flex-grow-1">
                                            <h6 class="mb-1 text-dark">${course.title}</h6>
                                            <p class="text-muted small mb-0">${course.category}</p>
                                            <p class="text-primary fw-bold small mb-0">${parseFloat(course.price).toLocaleString()} so'm</p>
                                        </div>
                                    </div>
                                </div>
                            </a>
                        `).join('');
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = '<div class="p-3 text-muted">Kurslar topilmadi</div>';
                        searchResults.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Search error:', error);
                });
        }, 300);
    });
    
    // Hide search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}
