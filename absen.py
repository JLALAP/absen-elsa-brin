import os
import sys
import time
import random
import argparse
from datetime import datetime
from playwright.sync_api import sync_playwright

from config import (
    ELSA_EMAIL,
    ELSA_PASSWORD,
    URL_LOGIN,
    URL_BERANDA,
    USER_AGENT,
    get_natural_coordinates
)
from auto_login import login_elsa, get_credentials

def parse_args():
    parser = argparse.ArgumentParser(description="Otomasi Presensi ELSA BRIN")
    parser.add_argument(
        "--mode",
        choices=["pagi", "sore", "datang", "pulang"],
        default="pagi",
        help="Mode absensi: pagi (datang) atau sore (pulang)"
    )
    parser.add_argument(
        "--skip-delay",
        action="store_true",
        help="Lewati jeda acak manusiawi (berguna saat pengujian manual)"
    )
    return parser.parse_args()

def apply_human_jitter(skip_delay=False):
    """
    Simulasi jeda acak manusiawi 1 s/d 8 menit (60 - 480 detik)
    agar jam presensi tidak tercatat di detik/menit yang sama setiap hari.
    """
    if skip_delay or os.environ.get("SKIP_DELAY", "").lower() == "true":
        print("[*] Jeda acak dilewati (mode testing).")
        return

    delay_seconds = random.randint(60, 480)
    delay_minutes = round(delay_seconds / 60, 1)
    print(f"[*] Menerapkan jeda acak manusiawi selama {delay_seconds} detik (~{delay_minutes} menit)...")
    time.sleep(delay_seconds)
    print("[*] Waktu jeda selesai, memulai proses presensi.")

def lakukan_presensi(page, mode):
    """
    Navigasi ke modul presensi / logbook magang dan klik tombol absen datang/pulang.
    """
    print(f"[*] Mencari modul presensi untuk mode: {mode.upper()}...")
    
    # Berikan waktu agar dashboard ELSA selesai me-render menu pengguna
    page.wait_for_timeout(3000)

    # 1. Cari tautan / menu menuju ke Presensi, Magang, atau Logbook
    target_keywords = ["presensi", "kehadiran", "magang", "logbook", "absen"]
    presensi_found = False

    # Coba telusuri elemen link dan tombol yang relevan
    elements = page.locator("a, button, div.card, li")
    count = elements.count()
    for i in range(min(count, 50)):
        el = elements.nth(i)
        try:
            txt = el.inner_text().strip().lower()
            if any(k in txt for k in target_keywords):
                href = el.get_attribute("href")
                print(f"[*] Ditemukan elemen terkait presensi: '{txt}' -> {href}")
        except Exception:
            pass

    # 2. Cari tombol aksi presensi (Datang / Pulang)
    tombol_target = []
    if mode in ["pagi", "datang"]:
        tombol_target = ["absen datang", "datang", "presensi datang", "check in", "masuk"]
    else:
        tombol_target = ["absen pulang", "pulang", "presensi pulang", "check out", "keluar"]

    clicked = False
    for label in tombol_target:
        btn = page.locator(f"button:has-text('{label}'), a:has-text('{label}'), input[value*='{label}']")
        if btn.count() > 0 and btn.first.is_visible():
            print(f"[+] Menemukan tombol presensi: '{label}'. Menekan tombol...")
            btn.first.click()
            clicked = True
            page.wait_for_timeout(3000)
            break

    # Ambil screenshot bukti absensi
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"bukti_absen_{mode}_{timestamp}.png"
    page.screenshot(path=screenshot_name, full_page=True)
    print(f"[+] Screenshot bukti presensi disimpan: {screenshot_name}")

    if clicked:
        print(f"[SUKSES] Presensi {mode.upper()} berhasil dieksekusi!")
        return True
    else:
        print(f"[*] Informasi: Tombol spesifik '{mode}' tidak langsung ditemukan di halaman utama.")
        print("[*] Halaman saat ini telah disimpan ke screenshot untuk verifikasi struktur menu akun Anda.")
        return False

def main():
    args = parse_args()
    print("=" * 60)
    print(f"   OTOMASI PRESENSI ELSA BRIN - MODE {args.mode.upper()}")
    print("=" * 60)
    print(f"Waktu Mulai : {datetime.now().strftime('%Y-%m-%d %H:%M:%S WIB')}")

    # Ambil kredensial
    email, password = get_credentials()
    if not email or not password:
        print("[X] ERROR: Kredensial ELSA_EMAIL dan ELSA_PASSWORD belum dikonfigurasi!")
        sys.exit(1)

    # Terapkan jeda manusiawi jika berjalan di cloud
    is_ci = os.environ.get("GITHUB_ACTIONS") == "true"
    apply_human_jitter(skip_delay=args.skip_delay or not is_ci)

    # Koordinat acak di KST BJ Habibie Serpong
    lat, lon = get_natural_coordinates()
    print(f"[*] Lokasi GPS Disimulasikan: {lat}, {lon} (Radius KST BJ Habibie Serpong)")

    with sync_playwright() as p:
        # Jalankan headless jika di CI / GitHub Actions, tampilkan browser jika lokal
        headless = is_ci or os.environ.get("HEADLESS", "false").lower() == "true"
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent=USER_AGENT,
            geolocation={"latitude": lat, "longitude": lon},
            permissions=["geolocation"],
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        try:
            # 1. Login ke sistem
            login_success = login_elsa(page, email, password)
            if not login_success:
                print("[X] Gagal melewati proses autentikasi SSO.")
                sys.exit(1)

            # 2. Eksekusi Presensi
            lakukan_presensi(page, args.mode)

        except Exception as e:
            print(f"[X] Terjadi kendala saat eksekusi: {e}")
            page.screenshot(path=f"error_{args.mode}_{int(time.time())}.png")
            sys.exit(1)
        finally:
            browser.close()

    print(f"[*] Selesai pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S WIB')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
