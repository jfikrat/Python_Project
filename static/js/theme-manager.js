/**
 * Theme Manager
 * Handles dark/light mode switching
 * No localStorage - resets to default (dark) on page reload
 */

class ThemeManager {
    constructor() {
        this.currentTheme = 'dark'; // Default theme
        this.toggleBtn = null;
        this.init();
    }

    /**
     * Initialize theme manager
     */
    init() {
        // Set initial theme
        this.setTheme(this.currentTheme);

        // Setup toggle button when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupToggleButton());
        } else {
            this.setupToggleButton();
        }
    }

    /**
     * Setup theme toggle button
     */
    setupToggleButton() {
        this.toggleBtn = document.getElementById('themeToggle');

        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggleTheme());
        }
    }

    /**
     * Set theme
     */
    setTheme(theme) {
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);

        // Add switching animation class
        if (this.toggleBtn) {
            this.toggleBtn.classList.add('switching');
            setTimeout(() => {
                this.toggleBtn.classList.remove('switching');
            }, 300);
        }

        // Refresh Lucide icons to ensure they render correctly with new theme
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    /**
     * Toggle between dark and light themes
     */
    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    /**
     * Get current theme
     */
    getCurrentTheme() {
        return this.currentTheme;
    }
}

// Initialize theme manager (single instance)
const themeManager = new ThemeManager();

// Export for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = themeManager;
}
