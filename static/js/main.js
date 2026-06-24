/**
 * Digital Saathi – Main JavaScript
 * Accessibility features and global UI interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize internationalization
    I18n.init();

    // Large text mode toggle (accessibility for elders)
    const largeTextToggle = document.getElementById('largeTextToggle');
    const savedLargeText = localStorage.getItem('saathi_large_text') === 'true';

    if (savedLargeText) {
        document.body.classList.add('large-text');
        if (largeTextToggle) largeTextToggle.setAttribute('aria-pressed', 'true');
    }

    if (largeTextToggle) {
        largeTextToggle.addEventListener('click', () => {
            const isLarge = document.body.classList.toggle('large-text');
            localStorage.setItem('saathi_large_text', isLarge);
            largeTextToggle.setAttribute('aria-pressed', isLarge);
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Auto-dismiss flash alerts after 5 seconds
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });
});
