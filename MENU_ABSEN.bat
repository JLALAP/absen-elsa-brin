@echo off
title ELSA BRIN - Assistant & Tool Otomasi Multi-User
color 0B
chcp 65001 >nul
cd /d "%~dp0"

:DETECT_PYTHON
set PYTHON_PATH=python
where python >nul 2>&1
if %errorlevel% neq 0 (
    if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    ) else (
        echo [PERINGATAN] Python belum terdeteksi di PATH sistem.
        echo Pastikan Python sudah terinstal di komputer Anda.
    )
)

:MENU
cls
echo ========================================================
echo        OTOMASI PRESENSI ELSA BRIN (MENU UTAMA)
echo ========================================================
echo.
echo  [1] Install Semua Kebutuhan (Playwright, OCR, Pillow)
echo  [2] Tes Absen PAGI Sekarang (Laptop Lokal)
echo  [3] Tes Absen SORE Sekarang (Laptop Lokal)
echo  [4] Tes Login Otomatis + Baca CAPTCHA
echo.
echo  --- PENGATURAN OTOMATIS LAPTOP (TANPA BAYAR / GRATIS) ---
echo  [5] Simpan Email ^& Password Akun Anda (Tersimpan Aman di Laptop)
echo  [6] Pasang / Aktifkan Jadwal Otomatis Windows (07:58 ^& 16:00 WIB)
echo  [7] Buka Halaman Presensi ELSA BRIN di Browser
echo  [0] Keluar
echo.
echo ========================================================
set /p opt="Pilih nomor menu [0-7]: "

if "%opt%"=="1" goto INSTALL
if "%opt%"=="2" goto ABSEN_PAGI
if "%opt%"=="3" goto ABSEN_SORE
if "%opt%"=="4" goto TEST_CAPTCHA
if "%opt%"=="5" goto SAVE_ENV
if "%opt%"=="6" goto SETUP_SCHEDULE
if "%opt%"=="7" goto OPEN_WEB
if "%opt%"=="0" exit
goto MENU

:INSTALL
cls
echo [INFO] Menginstal library yang dibutuhkan...
%PYTHON_PATH% -m pip install playwright ddddocr Pillow
%PYTHON_PATH% -m playwright install chromium
echo.
echo [SUKSES] Instalasi selesai!
pause
goto MENU

:ABSEN_PAGI
cls
echo [INFO] Menjalankan Absen PAGI...
%PYTHON_PATH% absen.py --mode pagi
pause
goto MENU

:ABSEN_SORE
cls
echo [INFO] Menjalankan Absen SORE...
%PYTHON_PATH% absen.py --mode sore
pause
goto MENU

:TEST_CAPTCHA
cls
echo [INFO] Menguji coba login mandiri & pemecah CAPTCHA...
%PYTHON_PATH% auto_login.py
pause
goto MENU

:SAVE_ENV
cls
echo ========================================================
echo        SIMPAN EMAIL & PASSWORD KE FILE LOKAL (.env)
echo ========================================================
echo Password hanya disimpan di laptop Anda sendiri (tidak di-upload ke internet).
echo.
set /p input_email="Masukkan Email ELSA BRIN: "
set /p input_pass="Masukkan Password ELSA BRIN: "

if "%input_email%"=="" (
    echo [!] Email tidak boleh kosong.
    pause
    goto MENU
)
if "%input_pass%"=="" (
    echo [!] Password tidak boleh kosong.
    pause
    goto MENU
)

echo ELSA_EMAIL=%input_email%> "%~dp0.env"
echo ELSA_PASSWORD=%input_pass%>> "%~dp0.env"

echo.
echo [SUKSES] Akun berhasil disimpan ke file .env di laptop Anda!
echo Mulai sekarang, jadwal otomatis dapat berjalan tanpa perlu mengetik password lagi.
pause
goto MENU

:SETUP_SCHEDULE
cls
echo [INFO] Memasang Jadwal Otomatis di Windows Task Scheduler...
powershell -ExecutionPolicy Bypass -File "%~dp0setup_jadwal.ps1"
echo.
echo [SELESAI] Komputer Anda sudah dijadwalkan otomatis absen jam 07:58 WIB & 16:00 WIB!
pause
goto MENU

:OPEN_WEB
start https://elsa.brin.go.id/akun
goto MENU
