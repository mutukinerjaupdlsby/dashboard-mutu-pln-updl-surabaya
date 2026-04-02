# HELPERS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.config import MONTHS_INDONESIA, DAMPAK_ORDER, STOP_WORDS
import re
from collections import Counter
from utils.config import STOP_WORDS

# format tanggal
def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f} detik"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} menit"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} jam"
    else:
        days = seconds / 86400
        return f"{days:.1f} hari"

# Get data dari bulan sebelumnya
def get_previous_month_data(df, current_month):
    if current_month == "Semua Bulan":
        return df, "Data keseluruhan"
    current_idx = MONTHS_INDONESIA.index(current_month) if current_month in MONTHS_INDONESIA else -1
    if current_idx <= 0:
        previous_month = "Desember"
    else:
        previous_month = MONTHS_INDONESIA[current_idx - 1]
    previous_df = df[df["Bulan"] == previous_month] if "Bulan" in df.columns else pd.DataFrame()
    return previous_df, previous_month

# Calculate trend
def calculate_trend(current_value, previous_value):
    if previous_value == 0 or pd.isna(previous_value):
        return 0, "neutral"
    change = ((current_value - previous_value) / previous_value) * 100
    if change > 0:
        return change, "up"
    elif change < 0:
        return abs(change), "down"
    else:
        return 0, "neutral"

# Validasi teks di NLP
def is_valid_text(text):
    if pd.isna(text):
        return False
    text_str = str(text).strip()
    
    invalid_patterns = ["", "-", ".", "...", "..", "null", "NaN", "none", "N/A", "n/a"]
    if text_str.lower() in invalid_patterns:
        return False
    
    word_count = len(text_str.split())
    char_count = len(text_str.replace(" ", ""))
    
    # EDIT SESUAI KEBUTUHAN (at least 5 words OR at least 20 characters)
    if word_count >= 5 or char_count >= 20:
        return True
    
    return False

# Warna bar chart dari sentimen
def get_bar_color(filter_option):
    if filter_option == "Positif":
        return "#28a745"
    elif filter_option == "Netral":
        return "#ffc107"
    elif filter_option == "Negatif":
        return "#dc3545"
    else:
        return "#0078d4"

# Warna wordcloud dari sentimen
def get_wordcloud_colormap(filter_option):
    if filter_option == "Positif":
        return "Greens"
    elif filter_option == "Netral":
        return "Wistia"
    elif filter_option == "Negatif":
        return "Reds"
    else:
        return "Blues"

# Warna Sentimen
def color_sentiment(val):
    if val == "Positif":
        return 'background-color: #28a74520; color: #28a745; font-weight: bold;'
    elif val == "Netral":
        return 'background-color: #ffc10720; color: #ffc107; font-weight: bold;'
    elif val == "Negatif":
        return 'background-color: #dc354520; color: #dc3545; font-weight: bold;'
    elif val == "Invalid":
        return 'background-color: #6c757d20; color: #6c757d; font-style: italic;'
    return ''

# Warna untuk nilai
def color_nilai(val):
    try:
        if isinstance(val, (int, float)) and pd.notna(val):
            if val >= 85:
                return 'background-color: #28a74520; color: #28a745;'
            elif val >= 70:
                return 'background-color: #ffc10720; color: #ffc107;'
            elif val < 70:
                return 'background-color: #dc354520; color: #dc3545;'
    except:
        pass
    return ''

# Sort dampak
def sort_dampak(dampak_list):
    if not dampak_list:
        return []
    # Filter hanya nilai dampak yang valid
    valid_dampak = [d for d in dampak_list if d in DAMPAK_ORDER]
    # Sort berdasarkan DAMPAK_ORDER
    sorted_dampak = sorted(valid_dampak, key=lambda x: DAMPAK_ORDER.index(x))
    unknown_dampak = [d for d in dampak_list if d not in DAMPAK_ORDER]
    
    return sorted_dampak + unknown_dampak

# Proses teks pada wordcloud
def process_text_for_wordcloud(text, remove_stopwords=True):
    if not text or not isinstance(text, str):
        return ""
    text = text.lower()
    words = text.split()
    if remove_stopwords:
        words = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return " ".join(words)

# Format angka
def format_angka(val, decimals=2):
    try:
        if pd.isna(val):
            return "-"
        if isinstance(val, (int, float)):
            return f"{val:.{decimals}f}"
        return str(val)
    except:
        return str(val)

# Clean text untuk proses NLP
def clean_text(text):
    if pd.isna(text):
        return ""
    
    import re
    text = str(text)
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Ekstrak keyword dari teks
def extract_keywords(text, top_n=10):
    from collections import Counter
    
    if not text or not isinstance(text, str):
        return []
    
    cleaned_text = clean_text(text)
    words = cleaned_text.lower().split()
    
    # Filter stop words
    filtered_words = [w for w in words if w not in STOP_WORDS and len(w) > 3]
    
    # Count frequency
    word_counts = Counter(filtered_words)
    
    # top N keywords
    return word_counts.most_common(top_n)

# hitung statistik sentimen
def calculate_sentiment_stats(df):
    if df.empty or "Sentimen" not in df.columns:
        return {
            "total": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "positive_pct": 0,
            "neutral_pct": 0,
            "negative_pct": 0,
            "dominant": "Tidak Ada"
        }
    
    total = len(df)
    positive = len(df[df["Sentimen"] == "Positif"])
    neutral = len(df[df["Sentimen"] == "Netral"])
    negative = len(df[df["Sentimen"] == "Negatif"])
    
    positive_pct = (positive / total * 100) if total > 0 else 0
    neutral_pct = (neutral / total * 100) if total > 0 else 0
    negative_pct = (negative / total * 100) if total > 0 else 0
    
    # Determine dominant sentiment
    counts = {"Positif": positive, "Netral": neutral, "Negatif": negative}
    dominant = max(counts, key=counts.get) if total > 0 else "Tidak Ada"
    
    return {
        "total": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "positive_pct": positive_pct,
        "neutral_pct": neutral_pct,
        "negative_pct": negative_pct,
        "dominant": dominant
    }

# filter berdasarkan date range
def filter_by_date_range(df, date_column, start_date, end_date):
    if date_column not in df.columns:
        return df
    
    if df[date_column].isna().all():
        return df
    
    df_filtered = df.copy()
    df_filtered[date_column] = pd.to_datetime(df_filtered[date_column], errors='coerce')
    
    if start_date:
        df_filtered = df_filtered[df_filtered[date_column] >= pd.to_datetime(start_date)]
    if end_date:
        df_filtered = df_filtered[df_filtered[date_column] <= pd.to_datetime(end_date)]
    
    return df_filtered

# Ekstrak data menjadi month-year
def get_month_year_from_date(df, date_column):
    if date_column not in df.columns:
        return df
    
    df_copy = df.copy()
    df_copy[date_column] = pd.to_datetime(df_copy[date_column], errors='coerce')
    df_copy['Month-Year'] = df_copy[date_column].dt.strftime('%b-%Y')
    df_copy['Month-Year_Sort'] = df_copy[date_column].dt.to_period('M')
    
    return df_copy

# clean text
def clean_text_for_words(text):
    if not text or not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Get top word
def get_top_words(text, top_n=10, remove_stopwords=True):
    if not text:
        return []

    cleaned_text = clean_text_for_words(text)
    if not cleaned_text:
        return []
    words = cleaned_text.split()
    if remove_stopwords:
        words = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    word_counts = Counter(words)

    return word_counts.most_common(top_n)

# prcess teks untuk wordcloud
def process_text_for_wordcloud(text, remove_stopwords=True):
    if not text or not isinstance(text, str):
        return ""
    cleaned_text = clean_text_for_words(text)
    
    if remove_stopwords:
        words = cleaned_text.split()
        words = [w for w in words if w not in STOP_WORDS and len(w) > 2]
        cleaned_text = " ".join(words)
    
    return cleaned_text