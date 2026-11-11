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
echo  [5] Simpan ^& Kirim Pembaruan ke GitHub (Auto Push)
echo.
echo  --- PANDUAN CEPAT SETUP CLOUD (UNTUK PENGGUNA BARU) ---
echo  [6] Buka Halaman Input Secrets di GitHub Repositori Anda
echo  [7] Buat Personal Access Token (PAT) Baru di GitHub
echo  [8] Buka Dashboard cron-job.org (Pengatur Waktu Presisi)
echo  [9] Buka Halaman Presensi ELSA BRIN
echo  [0] Keluar
echo.
echo ========================================================
set /p opt="Pilih nomor menu [0-9]: "

if "%opt%"=="1" goto INSTALL
if "%opt%"=="2" goto ABSEN_PAGI
if "%opt%"=="3" goto ABSEN_SORE
if "%opt%"=="4" goto TEST_CAPTCHA
if "%opt%"=="5" goto PUSH_GIT
if "%opt%"=="6" goto OPEN_SECRETS_AUTO
if "%opt%"=="7" goto OPEN_PAT_NEW
if "%opt%"=="8" goto OPEN_CRONJOB
if "%opt%"=="9" goto OPEN_WEB
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

:PUSH_GIT
cls
echo [INFO] Menyimpan dan mengirim pembaruan ke GitHub...
git add .
set /p commit_msg="Masukkan pesan update (tekan Enter jika default): "
if "%commit_msg%"=="" set commit_msg=Update script otomatis presensi
git commit -m "%commit_msg%"
git push
echo.
echo [SELESAI] Kode berhasil disinkronkan ke GitHub Anda!
pause
goto MENU

:OPEN_SECRETS_AUTO
cls
echo [INFO] Mendeteksi URL repositori GitHub Anda saat ini...
for /f "tokens=*" %%a in ('git config --get remote.origin.url') do set REPO_URL=%%a

if "%REPO_URL%"=="" (
    echo [INFO] URL Git belum terkonfigurasi. Membuka halaman login GitHub...
    start https://github.com
    pause
    goto MENU
)

:: Bersihkan format git url jika berawalan git@ atau diakhiri .git
set REPO_URL=%REPO_URL:.git=%
set REPO_URL=%REPO_URL:git@github.com:=https://github.com/%
set REPO_URL=%REPO_URL:https://.*@github.com/=https://github.com/%

echo Membuka halaman Secrets untuk repositori: %REPO_URL%
start %REPO_URL%/settings/secrets/actions
goto MENU

:OPEN_PAT_NEW
start https://github.com/settings/tokens/new?description=cron-trigger^&scopes=repo,workflow
goto MENU

:OPEN_CRONJOB
start https://cron-job.org
goto MENU

:OPEN_WEB
start https://elsa.brin.go.id/akun
goto MENU
