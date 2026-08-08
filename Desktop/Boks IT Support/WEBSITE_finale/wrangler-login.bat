@echo off
REM ============================================================
REM  Einmaliger Cloudflare-Login fuer Wrangler
REM  Nach dem Doppelklick oeffnet sich der Browser -> "Allow" klicken.
REM  Danach laeuft deploy.bat immer ohne Rueckfrage.
REM ============================================================
cd /d "%~dp0"
echo.
echo   Cloudflare-Login wird geoeffnet...
echo   Bitte im Browser mit "Allow" bestaetigen.
echo.
npx wrangler login
echo.
echo   Login abgeschlossen. Fenster kann geschlossen werden.
pause
