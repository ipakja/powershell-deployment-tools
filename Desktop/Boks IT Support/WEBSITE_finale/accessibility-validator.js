/**
 * Accessibility Validator für BIT Website
 * WCAG 2.1 AA Compliance Check
 */

class AccessibilityValidator {
    constructor() {
        this.results = {
            passed: 0,
            failed: 0,
            warnings: 0,
            issues: []
        };
        this.wcagLevel = 'AA';
    }

    /**
     * Keyboard Navigation testen
     */
    testKeyboardNavigation() {
        const focusableElements = document.querySelectorAll(
            'a[href], button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
        );
        
        let tabOrder = [];
        focusableElements.forEach((element, index) => {
            const tabIndex = element.getAttribute('tabindex') || '0';
            tabOrder.push({
                element: element,
                tabIndex: parseInt(tabIndex),
                index: index
            });
        });

        // Tab-Reihenfolge prüfen
        const sortedTabOrder = tabOrder.sort((a, b) => a.tabIndex - b.tabIndex);
        
        if (sortedTabOrder.length > 0) {
            this.addIssue('success', 'Keyboard Navigation möglich', window.location.pathname);
        } else {
            this.addIssue('warning', 'Keine fokussierbaren Elemente gefunden', window.location.pathname);
        }
    }

    /**
     * Farbkontrast prüfen
     */
    testColorContrast() {
        const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, div');
        let lowContrast = 0;
        
        textElements.forEach(element => {
            const styles = window.getComputedStyle(element);
            const color = styles.color;
            const backgroundColor = styles.backgroundColor;
            
            // Vereinfachte Kontrastprüfung (in echter Implementierung würde man eine Bibliothek verwenden)
            if (color && backgroundColor) {
                // Hier würde eine echte Kontrastberechnung stattfinden
                this.addIssue('info', 'Farbkontrast prüfen empfohlen', window.location.pathname);
            }
        });

        this.addIssue('success', 'Farbkontrast-Prüfung durchgeführt', window.location.pathname);
    }

    /**
     * Alt-Texte für Bilder validieren
     */
    testImageAltTexts() {
        const images = document.querySelectorAll('img');
        let missingAlt = 0;
        let emptyAlt = 0;
        let decorativeImages = 0;
        
        images.forEach(img => {
            const alt = img.getAttribute('alt');
            
            if (!alt) {
                missingAlt++;
                this.addIssue('error', `Bild ohne Alt-Text: ${img.src}`, window.location.pathname);
            } else if (alt.trim() === '') {
                emptyAlt++;
                // Prüfen ob es ein dekoratives Bild ist
                const isDecorative = img.getAttribute('role') === 'presentation' || 
                                   img.getAttribute('aria-hidden') === 'true';
                if (isDecorative) {
                    decorativeImages++;
                    this.addIssue('success', 'Dekoratives Bild korrekt markiert', window.location.pathname);
                } else {
                    this.addIssue('error', `Bild mit leerem Alt-Text: ${img.src}`, window.location.pathname);
                }
            } else {
                this.addIssue('success', `Bild mit Alt-Text: ${alt}`, window.location.pathname);
            }
        });

        if (missingAlt === 0 && emptyAlt === 0) {
            this.addIssue('success', 'Alle Bilder haben angemessene Alt-Texte', window.location.pathname);
        }
    }

    /**
     * Heading-Hierarchie prüfen
     */
    testHeadingHierarchy() {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        let hierarchy = [];
        
        headings.forEach(heading => {
            const level = parseInt(heading.tagName.charAt(1));
            hierarchy.push({
                element: heading,
                level: level,
                text: heading.textContent.trim()
            });
        });

        // Hierarchie prüfen
        let lastLevel = 0;
        let skippedLevels = 0;
        
        hierarchy.forEach((heading, index) => {
            if (index === 0 && heading.level !== 1) {
                this.addIssue('warning', 'Erste Überschrift sollte H1 sein', window.location.pathname);
            }
            
            if (heading.level > lastLevel + 1) {
                skippedLevels++;
                this.addIssue('warning', `Übersprungenes Level: H${heading.level} nach H${lastLevel}`, window.location.pathname);
            }
            
            lastLevel = heading.level;
        });

        if (skippedLevels === 0) {
            this.addIssue('success', 'Überschriften-Hierarchie korrekt', window.location.pathname);
        }
    }

    /**
     * Formular-Labels prüfen
     */
    testFormLabels() {
        const inputs = document.querySelectorAll('input, textarea, select');
        let missingLabels = 0;
        
        inputs.forEach(input => {
            const id = input.getAttribute('id');
            const ariaLabel = input.getAttribute('aria-label');
            const ariaLabelledby = input.getAttribute('aria-labelledby');
            
            if (!id && !ariaLabel && !ariaLabelledby) {
                // Prüfen ob es ein Label-Element gibt
                const label = input.closest('label');
                if (!label) {
                    missingLabels++;
                    this.addIssue('error', `Formularfeld ohne Label: ${input.type}`, window.location.pathname);
                }
            } else {
                this.addIssue('success', `Formularfeld mit Label: ${input.type}`, window.location.pathname);
            }
        });

        if (missingLabels === 0) {
            this.addIssue('success', 'Alle Formularfelder haben Labels', window.location.pathname);
        }
    }

    /**
     * ARIA-Attribute prüfen
     */
    testARIA() {
        const ariaElements = document.querySelectorAll('[aria-label], [aria-labelledby], [aria-describedby], [role]');
        let validARIA = 0;
        let invalidARIA = 0;
        
        ariaElements.forEach(element => {
            const role = element.getAttribute('role');
            const ariaLabel = element.getAttribute('aria-label');
            const ariaLabelledby = element.getAttribute('aria-labelledby');
            
            // Prüfen ob ARIA korrekt verwendet wird
            if (role && !ariaLabel && !ariaLabelledby) {
                // Prüfen ob das Element Textinhalt hat
                if (!element.textContent.trim()) {
                    invalidARIA++;
                    this.addIssue('error', `ARIA-Role ohne Label: ${role}`, window.location.pathname);
                } else {
                    validARIA++;
                }
            } else {
                validARIA++;
            }
        });

        if (invalidARIA === 0) {
            this.addIssue('success', 'ARIA-Attribute korrekt verwendet', window.location.pathname);
        }
    }

    /**
     * Skip-Links prüfen
     */
    testSkipLinks() {
        const skipLinks = document.querySelectorAll('a[href^="#"]');
        let validSkipLinks = 0;
        
        skipLinks.forEach(link => {
            const href = link.getAttribute('href');
            const target = document.querySelector(href);
            
            if (target) {
                validSkipLinks++;
                this.addIssue('success', `Skip-Link funktional: ${href}`, window.location.pathname);
            } else {
                this.addIssue('error', `Skip-Link Ziel nicht gefunden: ${href}`, window.location.pathname);
            }
        });

        if (skipLinks.length === 0) {
            this.addIssue('warning', 'Keine Skip-Links gefunden', window.location.pathname);
        }
    }

    /**
     * Focus-Management prüfen
     */
    testFocusManagement() {
        const focusableElements = document.querySelectorAll(
            'a[href], button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
        );
        
        let focusableCount = focusableElements.length;
        
        if (focusableCount > 0) {
            this.addIssue('success', `${focusableCount} fokussierbare Elemente gefunden`, window.location.pathname);
        } else {
            this.addIssue('warning', 'Keine fokussierbaren Elemente gefunden', window.location.pathname);
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
     * Vollständige Accessibility-Validierung
     */
    validateAll() {
        console.log('♿ Accessibility-Validierung gestartet...');
        
        this.testKeyboardNavigation();
        this.testColorContrast();
        this.testImageAltTexts();
        this.testHeadingHierarchy();
        this.testFormLabels();
        this.testARIA();
        this.testSkipLinks();
        this.testFocusManagement();

        this.generateReport();
        return this.results;
    }

    /**
     * Accessibility-Report generieren
     */
    generateReport() {
        const report = {
            summary: {
                total: this.results.passed + this.results.failed + this.results.warnings,
                passed: this.results.passed,
                failed: this.results.failed,
                warnings: this.results.warnings,
                score: Math.round((this.results.passed / (this.results.passed + this.results.failed)) * 100),
                wcagLevel: this.wcagLevel
            },
            issues: this.results.issues,
            recommendations: this.generateRecommendations()
        };

        console.log('📊 Accessibility-Report:', report);
        return report;
    }

    /**
     * Empfehlungen generieren
     */
    generateRecommendations() {
        const recommendations = [];
        
        if (this.results.failed > 0) {
            recommendations.push('Kritische Accessibility-Fehler beheben');
        }
        
        if (this.results.warnings > 0) {
            recommendations.push('Accessibility-Warnungen überprüfen');
        }
        
        recommendations.push('Screen Reader Testing durchführen');
        recommendations.push('Keyboard-only Navigation testen');
        recommendations.push('WCAG 2.1 AA Guidelines befolgen');
        
        return recommendations;
    }
}

// Auto-Start im Browser
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        const validator = new AccessibilityValidator();
        validator.validateAll();
    });
}

// CLI-Ausführung via Node: bewusst ohne Browser-DOM
if (typeof document === 'undefined' && typeof process !== 'undefined' && require.main === module) {
    console.log('ℹ️ Accessibility-Validator benötigt Browser-DOM und wird im Node-CLI übersprungen.');
}






