import os
import random

# ==========================================
# KONFIGURASI AKUN & KREDENSIAL
# ==========================================
# Mengambil dari Environment Variable (GitHub Actions Secret) 
# atau diisi langsung / lewat file .env untuk pengetesan lokal.
ELSA_EMAIL = os.environ.get("ELSA_EMAIL", "")
ELSA_PASSWORD = os.environ.get("ELSA_PASSWORD", "")

# ==========================================
# KONFIGURASI URL RESMI
# ==========================================
URL_LOGIN = "https://elsa.brin.go.id/login/index"
URL_BERANDA = "https://elsa.brin.go.id"
URL_AKUN = "https://elsa.brin.go.id/akun"

# ==========================================
# SIMULASI GEOLOKASI (KST BJ HABIBIE SERPONG)
# ==========================================
# Koordinat Pusat Kawasan Sains dan Teknologi B.J. Habibie BRIN Serpong (Puspiptek):
# Lat: -6.3653, Lon: 106.6661
BASE_LAT = -6.365312
BASE_LON = 106.666145

def get_natural_coordinates():
    """
    Menghasilkan variasi koordinat acak natural (5 - 15 meter)
    agar jejak lokasi tidak statis kaku seperti bot.
    """
    # 0.00001 derajat lat/lon ~ 1.1 meter
    jitter_lat = random.uniform(-0.00008, 0.00008)
    jitter_lon = random.uniform(-0.00008, 0.00008)
    lat = round(BASE_LAT + jitter_lat, 6)
    lon = round(BASE_LON + jitter_lon, 6)
    return lat, lon

# ==========================================
# PENGATURAN BROWSER & USER AGENT
# ==========================================
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
