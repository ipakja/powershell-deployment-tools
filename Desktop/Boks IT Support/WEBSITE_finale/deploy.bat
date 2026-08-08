@echo off
REM ============================================================
REM  BIT - Boks IT Support  |  Deploy zu Cloudflare Pages
REM ------------------------------------------------------------
REM  Einmalig noetig:
REM    1) Node.js installiert (hast du, da Cursor lief)
REM    2) Einmal einloggen:  npx wrangler login
REM  Danach: einfach diese Datei doppelklicken.
REM  >>> Projektname unten pruefen/anpassen! <<<
REM ============================================================

set PROJECT=website

cd /d "%~dp0"
echo.
echo ============================================================
echo   Deploye aktuelle Website-Dateien zu Cloudflare Pages
echo   Projekt: %PROJECT%
echo ============================================================
echo.

set CI=1
set WRANGLER_SEND_METRICS=false
python scripts\build_site.py
if errorlevel 1 (
    echo FEHLER: Website-Build fehlgeschlagen.
    exit /b 1
)
echo n | npx wrangler pages deploy . --project-name=%PROJECT% --branch=main --commit-dirty=true
if errorlevel 1 (
    echo FEHLER: Cloudflare-Deployment fehlgeschlagen.
    exit /b 1
)

echo.
echo ------------------------------------------------------------
echo   Falls Fehler "project not found": richtigen Namen finden
echo   mit:   npx wrangler pages project list
echo   und oben bei set PROJECT=... eintragen.
echo ------------------------------------------------------------
echo.
echo Fertig. Fenster kann geschlossen werden.
pause
