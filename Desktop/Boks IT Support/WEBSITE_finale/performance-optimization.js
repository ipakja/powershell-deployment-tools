/**
 * Performance Optimization Script
 * Automatische Optimierung für BIT Website
 */

class PerformanceOptimizer {
    constructor() {
        this.optimizations = [];
        this.metrics = {};
    }

    /**
     * Lazy Loading für Bilder implementieren
     */
    optimizeImages() {
        const images = document.querySelectorAll('img[data-src]');
        
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

            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback für ältere Browser
            images.forEach(img => {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
            });
        }

        this.optimizations.push('Lazy Loading aktiviert');
    }

    /**
     * CSS Critical Path optimieren
     */
    optimizeCriticalCSS() {
        // Inline Critical CSS für Above-the-Fold Content
        const criticalCSS = `
            .hero { 
                background: var(--anthrazit); 
                min-height: 70vh; 
                display: flex; 
                align-items: center; 
            }
            .hero-text h1 { 
                font-size: 3rem; 
                color: var(--gold); 
                margin-bottom: 1rem; 
            }
            .btn { 
                background: var(--gold); 
                color: var(--anthrazit); 
                padding: 1rem 2rem; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
            }
        `;

        const style = document.createElement('style');
        style.textContent = criticalCSS;
        document.head.insertBefore(style, document.head.firstChild);

        this.optimizations.push('Critical CSS inline');
    }

    /**
     * JavaScript Lazy Loading
     */
    optimizeJavaScript() {
        // Non-critical JavaScript verzögert laden
        const nonCriticalScripts = [
            'js/animation-manager.js',
            'js/theme-manager.js'
        ];

        nonCriticalScripts.forEach(src => {
            const script = document.createElement('script');
            script.src = src;
            script.async = true;
            script.defer = true;
            document.body.appendChild(script);
        });

        this.optimizations.push('JavaScript Lazy Loading');
    }

    /**
     * Preload wichtige Ressourcen
     */
    preloadResources() {
        const preloadLinks = [
            { href: 'css/main.css', as: 'style' },
            { href: 'css/components.css', as: 'style' },
            { href: 'https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&family=Playfair+Display:wght@400;500;600;700&display=swap', as: 'style' }
        ];

        preloadLinks.forEach(link => {
            const preload = document.createElement('link');
            preload.rel = 'preload';
            preload.href = link.href;
            preload.as = link.as;
            document.head.appendChild(preload);
        });

        this.optimizations.push('Resource Preloading');
    }

    /**
     * Service Worker für Caching
     */
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('Service Worker registriert:', registration);
                })
                .catch(error => {
                    console.log('Service Worker Fehler:', error);
                });
        }
    }

    /**
     * Performance Metriken sammeln
     */
    collectMetrics() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    
                    this.metrics = {
                        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                        loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
                        totalTime: perfData.loadEventEnd - perfData.fetchStart
                    };

                    console.log('Performance Metriken:', this.metrics);
                }, 0);
            });
        }
    }

    /**
     * Alle Optimierungen ausführen
     */
    optimize() {
        this.optimizeImages();
        this.optimizeCriticalCSS();
        this.optimizeJavaScript();
        this.preloadResources();
        this.setupServiceWorker();
        this.collectMetrics();

        console.log('Performance Optimierungen:', this.optimizations);
        return this.metrics;
    }
}

// Auto-Start im Browser
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        const optimizer = new PerformanceOptimizer();
        optimizer.optimize();
    });
}

// CLI-Ausführung via Node: bewusst ohne Browser-DOM
if (typeof document === 'undefined' && typeof process !== 'undefined' && require.main === module) {
    console.log('ℹ️ Performance-Optimierung benötigt Browser-DOM und wird im Node-CLI übersprungen.');
}






