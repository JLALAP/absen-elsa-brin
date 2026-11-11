# Otomasi Presensi ELSA BRIN (Cloud + Lokal)

Sistem otomasi presensi pagi (08:00 WIB) dan sore (16:00 WIB) untuk portal ELSA BRIN.
Sistem berjalan 100% di server cloud (GitHub Actions + cron-job.org) atau bisa dijalankan langsung lewat laptop secara lokal.

## Fitur Utama
1. **AI Vision (ddddocr)**: Memecahkan CAPTCHA angka & huruf di SSO BRIN secara otomatis tanpa token berbayar.
2. **Simulasi GPS KST BJ Habibie Serpong**: Emulasi koordinat GPS presisi di kawasan Serpong dengan jitter acak alami 5-15 meter.
3. **Jeda Manusiawi**: Jeda waktu acak 1-8 menit sebelum submit presensi agar jam absen natural setiap harinya.
4. **Cloud Execution**: Menggunakan GitHub Actions gratisan yang dipicu oleh cron-job.org tepat waktu.

## Struktur File
- `MENU_ABSEN.bat` : Menu interaktif utama untuk menjalankan opsi lokal & cloud.
- `absen.py` : Script eksekutor presensi (`--mode pagi` atau `--mode sore`).
- `auto_login.py` : Script pengujian login & pembacaan CAPTCHA otomatis.
- `config.py` : Konfigurasi koordinat GPS dan URL portal.
- `.github/workflows/absen.yml` : Workflow cloud GitHub Actions.

## Panduan Penggunaan
Silakan buka file `MENU_ABSEN.bat` atau ikuti dokumen `Panduan_Lengkap_Otomasi_Presensi_ELSA_BRIN.pdf`.
