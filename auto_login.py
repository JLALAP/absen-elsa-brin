import os
import sys
import time
import getpass
from playwright.sync_api import sync_playwright
import ddddocr

from config import (
    ELSA_EMAIL,
    ELSA_PASSWORD,
    URL_LOGIN,
    USER_AGENT,
    get_natural_coordinates
)

def get_credentials():
    email = os.environ.get("ELSA_EMAIL", "") or ELSA_EMAIL
    password = os.environ.get("ELSA_PASSWORD", "") or ELSA_PASSWORD

    # Jika belum ada di environment variable / config, minta input interaktif
    if not email:
        email = input("Masukkan Email ELSA BRIN: ").strip()
    if not password:
        password = getpass.getpass("Masukkan Password ELSA BRIN: ").strip()
    
    return email, password

def solve_captcha(ocr_engine, page):
    """Mengambil screenshot elemen captcha dan membacanya via ddddocr."""
    try:
        captcha_el = page.locator("#img-captcha")
        captcha_el.wait_for(state="visible", timeout=10000)
        img_bytes = captcha_el.screenshot()
        result = ocr_engine.classification(img_bytes)
        clean_code = "".join(ch for ch in result if ch.isalnum())
        return clean_code
    except Exception as e:
        print(f"[!] Gagal mengekstrak CAPTCHA: {e}")
        return None

def login_elsa(page, email, password, max_retries=3):
    ocr = ddddocr.DdddOcr(show_ad=False)

    print(f"[*] Membuka halaman login: {URL_LOGIN}")
    page.goto(URL_LOGIN, wait_until="networkidle", timeout=60000)

    for attempt in range(1, max_retries + 1):
        print(f"[*] Percobaan login ke-{attempt}...")

        # Pastikan kita di halaman SSO login BRIN
        if "sso.brin.go.id" in page.url or page.locator("input[name='identity']").count() > 0:
            page.locator("input[name='identity']").fill(email)
            page.locator("input[name='password']").fill(password)

            # Centang persetujuan jika ada checkbox TOS
            tos_box = page.locator("input[name='checkbox_tos']")
            if tos_box.count() > 0 and not tos_box.is_checked():
                tos_box.check()

            # Selesaikan CAPTCHA
            captcha_text = solve_captcha(ocr, page)
            print(f"[*] OCR mendeteksi CAPTCHA: '{captcha_text}'")
            if captcha_text:
                page.locator("input[name='captcha']").fill(captcha_text)

            # Klik tombol submit login
            submit_btn = page.locator("button[type='submit']")
            if submit_btn.count() > 0:
                submit_btn.click()
            else:
                page.keyboard.press("Enter")

            # Tunggu respon setelah submit
            page.wait_for_timeout(3500)

            # Cek apakah berhasil login (redirect kembali ke elsa.brin.go.id)
            curr_url = page.url
            print(f"[*] URL setelah submit: {curr_url}")

            if "elsa.brin.go.id" in curr_url and "sso.brin.go.id" not in curr_url:
                print("[+] LOGIN BERHASIL! Berhasil dialihkan ke portal ELSA BRIN.")
                return True

            # Cek pesan error di halaman SSO
            error_alerts = page.locator(".alert, .text-red-500, .text-danger, .invalid-feedback")
            if error_alerts.count() > 0:
                msg = error_alerts.first.inner_text().strip()
                print(f"[!] Pesan respon sistem: {msg}")

            print("[-] Login belum berhasil, mencoba ulang...")
            page.wait_for_timeout(1000)
        else:
            if "elsa.brin.go.id" in page.url:
                print("[+] Sudah dalam sesi login.")
                return True
            page.goto(URL_LOGIN, wait_until="networkidle")

    print("[X] Gagal login setelah beberapa kali percobaan.")
    return False

def test_auto_login():
    email, password = get_credentials()
    if not email or not password:
        print("[!] Email atau password belum diisi. Pengetesan dibatalkan.")
        return

    lat, lon = get_natural_coordinates()
    print(f"[*] Menyiapkan browser dengan emulasi GPS Serpong ({lat}, {lon})...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=USER_AGENT,
            geolocation={"latitude": lat, "longitude": lon},
            permissions=["geolocation"],
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        success = login_elsa(page, email, password)
        if success:
            print("[SUKSES] Pengujian login otomatis dan OCR CAPTCHA berhasil sempurna!")
            page.wait_for_timeout(5000)
        else:
            print("[GAGAL] Login tidak berhasil. Mohon periksa kembali email & password Anda.")
            page.wait_for_timeout(3000)

        browser.close()

if __name__ == "__main__":
    test_auto_login()
