/**
 * Digital Saathi – Internationalization (i18n)
 * Loads translations and updates page text dynamically
 */

const I18n = {
    currentLang: 'en',
    translations: {},

    /**
     * Initialize i18n system on page load
     */
    async init() {
        // Get language from HTML data attribute or localStorage
        const htmlLang = document.documentElement.getAttribute('data-lang') || 'en';
        const savedLang = localStorage.getItem('saathi_lang');
        this.currentLang = savedLang || htmlLang;

        await this.loadTranslations(this.currentLang);
        this.applyTranslations();
        this.setupLanguageSelector();
    },

    /**
     * Fetch translation JSON from backend API
     */
    async loadTranslations(lang) {
        try {
            const response = await fetch(`/api/translations/${lang}`);
            this.translations = await response.json();
            this.currentLang = lang;
            localStorage.setItem('saathi_lang', lang);

            // Sync with server session
            await fetch('/api/set-language', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ language: lang })
            });
        } catch (error) {
            console.error('Failed to load translations:', error);
        }
    },

    /**
     * Apply translations to all elements with data-i18n attribute
     */
    applyTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (this.translations[key]) {
                el.textContent = this.translations[key];
            }
        });

        // Handle placeholder translations
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (this.translations[key]) {
                el.placeholder = this.translations[key];
            }
        });

        // Update HTML lang attribute
        document.documentElement.lang = this.currentLang;
    },

    /**
     * Get a single translation string
     */
    t(key) {
        return this.translations[key] || key;
    },

    /**
     * Setup language dropdown change handler
     */
    setupLanguageSelector() {
        const selector = document.getElementById('languageSelector');
        if (!selector) return;

        selector.value = this.currentLang;
        selector.addEventListener('change', async (e) => {
            await this.loadTranslations(e.target.value);
            this.applyTranslations();
        });
    }
};

// Export for use in other scripts
window.I18n = I18n;
