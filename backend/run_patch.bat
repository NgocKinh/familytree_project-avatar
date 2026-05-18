@echo off
setlocal

REM ==============================
REM CONFIG
REM ==============================
set MYSQL_BIN=mysql
set DB_HOST=localhost
set DB_PORT=3306
set DB_NAME=familytreedb
set DB_USER=root
set PATCH_FILE=patch_production_idempotent.sql

REM ==============================
REM CHECK PATCH FILE
REM ==============================
if not exist "%PATCH_FILE%" (
echo [ERROR] Khong tim thay file patch: %PATCH_FILE%
pause
exit /b 1
)

echo ==========================================
echo  APPLY PATCH TO %DB_NAME%
echo ==========================================
echo Host: %DB_HOST%:%DB_PORT%
echo User: %DB_USER%
echo File: %PATCH_FILE%
echo.

REM ==============================
REM RUN PATCH
REM ==============================
"%MYSQL_BIN%" -h %DB_HOST% -P %DB_PORT% -u %DB_USER% -p %DB_NAME% < "%PATCH_FILE%"

if errorlevel 1 (
echo.
echo [FAILED] Patch bi loi. Kiem tra thong bao o tren.
pause
exit /b 1
)

echo.
echo [OK] Patch da chay thanh cong.
pause
endlocal
