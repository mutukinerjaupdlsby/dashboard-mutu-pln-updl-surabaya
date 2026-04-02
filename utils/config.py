# CONFIGURATION
import os

# DATA BASED ON URL GSHEET
URL_EVALUASI_L1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDJgmkNt8qXd_q1GA0YwlL_vBt8INbOGgQyO_QhIJi6tq7ZlZlmZFOpmWInRtAbdkgIuedKD7-Jgk-/pub?gid=0&single=true&output=csv"
URL_PENILAIAN = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDJgmkNt8qXd_q1GA0YwlL_vBt8INbOGgQyO_QhIJi6tq7ZlZlmZFOpmWInRtAbdkgIuedKD7-Jgk-/pub?gid=804141987&single=true&output=csv"

# Model paths
SENTIMENT_MODEL_PATH = "sentiment_best_model"
INDIKATOR_MODEL_PATH = "indikator_best_model"
KELUHAN_MODEL_PATH = "keluhan_best_model"

# Color mapping
COLOR_MAP = {
    "Positif": "#28a745",
    "Netral": "#ffc107", 
    "Negatif": "#dc3545"
}

# Indikator dan Keluhan mapping
INDIKATOR_KELUHAN_MAP = {
    "K_Informasi": ["Adanya Informasi", "Media Penyampaian Informasi", "Kejelasan Informasi", "Ketepatan Waktu Informasi"],
    "K_Keterlibatan": ["Keterlibatan Di Kelas", "Paralel Dengan Kerjaan Rutin", "Waktu Pelaksanaan", "Keinteraktifan Metode Pelaksanaan"],
    "K_Suasana_Kelas": ["Lay Out Kelas", "Keinteraktifan Pembelajaran", "Paralel Dengan Kerjaan Rutin", "Lokasi Kelas"],
    "K_Materi": ["Kesesuaian Materi", "Kejelasan Materi", "Materi Terbaru", "Durasi Waktu Pembelajaran"],
    "K_Dampak": ["Kesesuaian Materi", "Penerapan Di Pekerjaan"],
    "K_Instruktur": ["Penyampaian Materi", "Keterlibatan Di Kelas", "Keinteraktifan Pembelajaran"],
    "K_Wisma": ["Kondisi Penginapan"],
    "K_Konsumsi": ["Kondisi Makanan"],
    "K_Pelayanan": ["Komunikatif", "Responsifitas", "Keaktifan Menyampaikan Informasi"],
    "K_Keandalan_Infrastruktur": ["Kondisi Jaringan", "Fasilitas Pembelajaran", "Penggunaan Web / LMS"],
    "K_Kemudahan_Akses": ["Penggunaan Web / LMS"],
    "K_Struktur_Website_Jelas_dan_Rapi": ["Penggunaan Web / LMS"],
    "K_Kefektifitasan_Menu_Navigasi": ["Penggunaan Web / LMS"],
    "K_Tampilan_Materi_Menarik": ["Materi Menarik"],
    "K_Manajemen_Waktu": ["Durasi Waktu Pembelajaran"],
    "K_Pelayanan_DL": ["Komunikatif", "Responsifitas", "Keaktifan Menyampaikan Informasi"]
}

# Month order for Indonesian
MONTHS_INDONESIA = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
# Dampak order
DAMPAK_ORDER = ['MINOR', 'MODERAT', 'SIGNIFIKAN', 'SANGAT SIGNIFIKAN']
# Nama halaman
PAGES = {
    "Evaluasi L1": "Evaluasi L1",
    "Penilaian": "Penilaian",
    "Sistem NLP": "Sistem NLP",
    "Info": "Info"
}

# Stop words for text processing
STOP_WORDS = ["#ok", "#", "ok", "yang", "di", "dan", "untuk", "dengan", "pada", "agar", "lebih", "dari", "ini", "itu", "ke", "dalam", "yg", "tdk", "tidak", "saya", "kita", "juga", "sudah", "akan", "bisa", "dapat", "sangat", "kurang", "cukup", "baik", "bagus"]