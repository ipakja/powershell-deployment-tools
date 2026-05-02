/**
 * SEO Validator für BIT Website
 * Automatische Überprüfung aller SEO-Kriterien
 */

class SEOValidator {
    constructor() {
        this.results = {
            passed: 0,
            failed: 0,
            warnings: 0,
            issues: []
        };
    }

    /**
     * Meta-Tags validieren
     */
    validateMetaTags() {
        const required = ['title', 'description', 'keywords'];
        const currentPage = window.location.pathname;
        
        required.forEach(tag => {
            const element = document.querySelector(`meta[name="${tag}"]`);
            if (!element || !element.content.trim()) {
                this.addIssue('error', `Meta-${tag} fehlt oder ist leer`, currentPage);
            } else {
                this.addIssue('success', `Meta-${tag} vorhanden`, currentPage);
            }
        });

        // Title-Länge prüfen
        const title = document.querySelector('title');
        if (title) {
            const titleLength = title.textContent.length;
            if (titleLength < 30) {
                this.addIssue('warning', `Title zu kurz (${titleLength} Zeichen)`, currentPage);
            } else if (titleLength > 60) {
                this.addIssue('warning', `Title zu lang (${titleLength} Zeichen)`, currentPage);
            } else {
                this.addIssue('success', `Title optimal (${titleLength} Zeichen)`, currentPage);
            }
        }

        // Description-Länge prüfen
        const description = document.querySelector('meta[name="description"]');
        if (description) {
            const descLength = description.content.length;
            if (descLength < 120) {
                this.addIssue('warning', `Description zu kurz (${descLength} Zeichen)`, currentPage);
            } else if (descLength > 160) {
                this.addIssue('warning', `Description zu lang (${descLength} Zeichen)`, currentPage);
            } else {
                this.addIssue('success', `Description optimal (${descLength} Zeichen)`, currentPage);
            }
        }
    }

    /**
     * Open Graph Tags validieren
     */
    validateOpenGraph() {
        const ogTags = ['og:title', 'og:description', 'og:type', 'og:url'];
        
        ogTags.forEach(tag => {
            const element = document.querySelector(`meta[property="${tag}"]`);
            if (!element || !element.content.trim()) {
                this.addIssue('error', `Open Graph ${tag} fehlt`, window.location.pathname);
            } else {
                this.addIssue('success', `Open Graph ${tag} vorhanden`, window.location.pathname);
            }
        });
    }

    /**
     * Strukturierte Daten validieren
     */
    validateStructuredData() {
        const jsonLd = document.querySelector('script[type="application/ld+json"]');
        if (!jsonLd) {
            this.addIssue('error', 'Strukturierte Daten (JSON-LD) fehlen', window.location.pathname);
        } else {
            try {
                const data = JSON.parse(jsonLd.textContent);
                if (data['@type'] && data.name) {
                    this.addIssue('success', 'Strukturierte Daten korrekt', window.location.pathname);
                } else {
                    this.addIssue('warning', 'Strukturierte Daten unvollständig', window.location.pathname);
                }
            } catch (error) {
                this.addIssue('error', 'Strukturierte Daten JSON-Fehler', window.location.pathname);
            }
        }
    }

    /**
     * Heading-Struktur validieren
     */
    validateHeadings() {
        const h1 = document.querySelectorAll('h1');
        const h2 = document.querySelectorAll('h2');
        
        if (h1.length === 0) {
            this.addIssue('error', 'H1-Tag fehlt', window.location.pathname);
        } else if (h1.length > 1) {
            this.addIssue('warning', 'Mehrere H1-Tags gefunden', window.location.pathname);
        } else {
            this.addIssue('success', 'H1-Tag korrekt', window.location.pathname);
        }

        if (h2.length === 0) {
            this.addIssue('warning', 'Keine H2-Tags gefunden', window.location.pathname);
        } else {
            this.addIssue('success', `${h2.length} H2-Tags gefunden`, window.location.pathname);
        }
    }

    /**
     * Alt-Tags für Bilder validieren
     */
    validateImages() {
        const images = document.querySelectorAll('img');
        let missingAlt = 0;
        
        images.forEach(img => {
            if (!img.alt || img.alt.trim() === '') {
                missingAlt++;
            }
        });

        if (missingAlt > 0) {
            this.addIssue('warning', `${missingAlt} Bilder ohne Alt-Text`, window.location.pathname);
        } else {
            this.addIssue('success', 'Alle Bilder haben Alt-Text', window.location.pathname);
        }
    }

    /**
     * Links validieren
     */
    validateLinks() {
        const links = document.querySelectorAll('a[href]');
        let brokenLinks = 0;
        let externalLinks = 0;
        
        links.forEach(link => {
            const href = link.getAttribute('href');
            
            // Externe Links prüfen
            if (href.startsWith('http') && !href.includes(window.location.hostname)) {
                externalLinks++;
                if (!link.hasAttribute('rel') || !link.getAttribute('rel').includes('nofollow')) {
                    this.addIssue('info', 'Externer Link ohne nofollow', window.location.pathname);
                }
            }
        });

        this.addIssue('info', `${externalLinks} externe Links gefunden`, window.location.pathname);
    }

    /**
     * Mobile-Freundlichkeit prüfen
     */
    validateMobile() {
        const viewport = document.querySelector('meta[name="viewport"]');
        if (!viewport) {
            this.addIssue('error', 'Viewport Meta-Tag fehlt', window.location.pathname);
        } else {
            this.addIssue('success', 'Viewport Meta-Tag vorhanden', window.location.pathname);
        }

        // Touch-Icons prüfen
        const touchIcon = document.querySelector('link[rel="apple-touch-icon"]');
        if (!touchIcon) {
            this.addIssue('warning', 'Apple Touch Icon fehlt', window.location.pathname);
        } else {
            this.addIssue('success', 'Apple Touch Icon vorhanden', window.location.pathname);
        }
    }

    /**
     * Performance-Indikatoren
     */
    validatePerformance() {
        // Lazy Loading
        const lazyImages = document.querySelectorAll('img[data-src]');
        if (lazyImages.length > 0) {
            this.addIssue('success', 'Lazy Loading implementiert', window.location.pathname);
        }

        // Service Worker
        if ('serviceWorker' in navigator) {
            this.addIssue('success', 'Service Worker unterstützt', window.location.pathname);
        }
    }

    /**
     * Issue hinzufügen
     */
    addIssue(type, message, page) {
        this.results.issues.push({
            type: type,
            message: message,
            page: page,
            timestamp: new Date().toISOString()
        });

        switch (type) {
            case 'success':
                this.results.passed++;
                break;
            case 'error':
                this.results.failed++;
                break;
            case 'warning':
                this.results.warnings++;
                break;
        }
    }

    /**
     * Vollständige SEO-Validierung
     */
    validateAll() {
        console.log('🔍 SEO-Validierung gestartet...');
        
        this.validateMetaTags();
        this.validateOpenGraph();
        this.validateStructuredData();
        this.validateHeadings();
        this.validateImages();
        this.validateLinks();
        this.validateMobile();
        this.validatePerformance();

        this.generateReport();
        return this.results;
    }

    /**
     * SEO-Report generieren
     */
    generateReport() {
        const report = {
            summary: {
                total: this.results.passed + this.results.failed + this.results.warnings,
                passed: this.results.passed,
                failed: this.results.failed,
                warnings: this.results.warnings,
                score: Math.round((this.results.passed / (this.results.passed + this.results.failed)) * 100)
            },
            issues: this.results.issues,
            recommendations: this.generateRecommendations()
        };

        console.log('📊 SEO-Report:', report);
        return report;
    }

    /**
     * Empfehlungen generieren
     */
    generateRecommendations() {
        const recommendations = [];
        
        if (this.results.failed > 0) {
            recommendations.push('Kritische SEO-Fehler beheben');
        }
        
        if (this.results.warnings > 0) {
            recommendations.push('SEO-Warnungen überprüfen');
        }
        
        recommendations.push('Regelmäßige SEO-Überwachung einrichten');
        recommendations.push('Google Search Console konfigurieren');
        
        return recommendations;
    }
}

// Auto-Start im Browser
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        const validator = new SEOValidator();
        validator.validateAll();
    });
}

// CLI-Ausführung via Node: bewusst ohne Browser-DOM
if (typeof document === 'undefined' && typeof process !== 'undefined' && require.main === module) {
    console.log('ℹ️ SEO-Validator benötigt Browser-DOM und wird im Node-CLI übersprungen.');
}






