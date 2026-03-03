document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle Logic
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const currentTheme = localStorage.getItem('theme') || 'light';

    // Apply saved theme
    if (currentTheme === 'dark') {
        body.setAttribute('data-theme', 'dark');
        themeToggle.innerHTML = '<i class="bi bi-sun-fill text-warning"></i>';
    }

    themeToggle.addEventListener('click', () => {
        const theme = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        if (theme === 'dark') {
            themeToggle.innerHTML = '<i class="bi bi-sun-fill text-warning"></i>';
        } else {
            themeToggle.innerHTML = '<i class="bi bi-moon-stars"></i>';
        }
    });

    // Loading Spinner on Form Submits
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', () => {
            const spinner = document.getElementById('loading-spinner');
            if (spinner) spinner.classList.remove('d-none');
            if (spinner) spinner.classList.add('d-flex');
        });
    });
});

// Delete Confirmation
function confirmDelete(event) {
    if (!confirm('Are you sure you want to delete this task?')) {
        event.preventDefault();
        return false;
    }
    return true;
}
