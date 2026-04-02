# SISTEM NLP
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import time
from datetime import datetime
from io import BytesIO
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    load_sentiment_model, predict_sentiment,
    load_indikator_model, load_indikator_labels, predict_indikator,
    load_keluhan_model, load_keluhan_labels, predict_keluhan, validate_keluhan_with_indikator
)

from utils.helpers import format_time, is_valid_tex

def process_data_nlp(df):
    start_time = time.time()

    tokenizer_sent, model_sent = load_sentiment_model()
    tokenizer_ind, model_ind = load_indikator_model()
    tokenizer_kel, model_kel = load_keluhan_model()

    label_map_ind = load_indikator_labels()
    label_map_kel = load_keluhan_labels()

    labels, confidences = [], []
    indikator_labels, indikator_confs = [], []
    keluhan_labels, keluhan_confs = [], []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, text in enumerate(df["Komentar"]):
        if is_valid_text(text):
            sent_label, sent_conf = predict_sentiment(str(text), tokenizer_sent, model_sent)
            ind_label, ind_conf = predict_indikator(str(text), tokenizer_ind, model_ind, label_map_ind)
            kel_label, kel_conf = predict_keluhan(str(text), tokenizer_kel, model_kel, label_map_kel)

            kel_label = validate_keluhan_with_indikator(ind_label, kel_label)

        else:
            sent_label, sent_conf = "Invalid", None
            ind_label, ind_conf = "Invalid", None
            kel_label, kel_conf = "Invalid", None

        labels.append(sent_label)
        confidences.append(sent_conf)
        indikator_labels.append(ind_label)
        indikator_confs.append(ind_conf)
        keluhan_labels.append(kel_label)
        keluhan_confs.append(kel_conf)

        progress_bar.progress((i + 1) / len(df))
        status_text.text(f"Memproses data ke-{i+1} dari {len(df)}")

    df["Sentimen"] = labels
    df["Confidence"] = confidences
    df["Indikator"] = indikator_labels
    df["Indikator Confidence"] = indikator_confs
    df["Keluhan"] = keluhan_labels
    df["Keluhan Confidence"] = keluhan_confs

    progress_bar.empty()
    status_text.empty()

    st.session_state.df = df
    st.session_state.processing_time = time.time() - start_time
    st.session_state.analysis_done = Tru


def format_percentage(x):
    try:
        return f"{float(x):.2%}"
    except:
        return "-

def render_sistem_nlp():

    st.markdown("""
    <div class='page-header'>
        <h1 class='page-title'>💬 Sistem NLP</h1>
        <p class='page-description'>Analisis Sentimen, Indikator, dan Keluhan</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📁 Import File", "📝 Input Teks"]
    # TAB
    with tab1:

        uploaded = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

        if uploaded is None:
            st.session_state.clear()

        if uploaded:
            df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)

            st.dataframe(df.head(), use_container_width=True)

            if "Komentar" not in df.columns:
                st.error("Harus ada kolom 'Komentar'")
            else:
                if st.button("🔍 Analisis NLP", use_container_width=True):
                    process_data_nlp(df)
                    st.rerun()
                    
        # HASIL ANALISIS
        if st.session_state.get("analysis_done"):

            df = st.session_state.df.copy()

            df_valid = df[df["Sentimen"] != "Invalid"]
            total = len(df_valid)

            pos = (df_valid["Sentimen"] == "Positif").sum()
            neu = (df_valid["Sentimen"] == "Netral").sum()
            neg = (df_valid["Sentimen"] == "Negatif").sum()

            st.success(f"Total Data Valid: {total}")

            # CHART
            if total > 0:
                sentiment_counts = df_valid["Sentimen"].value_counts().reset_index()
                sentiment_counts.columns = ["Sentimen", "Jumlah"]

                chart = alt.Chart(sentiment_counts).mark_bar().encode(
                    x="Sentimen",
                    y="Jumlah",
                    color="Sentimen"
                )

                st.altair_chart(chart, use_container_width=True)

            # TABLE 
            if "analysis_done" in st.session_state and st.session_state.analysis_done and "df" in st.session_state:
                result_data = st.session_state.df.copy()
                for col_conf in ['Confidence', 'Indikator Confidence', 'Keluhan Confidence']:
                    if col_conf in result_data.columns:
                        result_data[col_conf] = result_data[col_conf].apply(
                            lambda x: f"{float(x):.2%}" if pd.notna(x) else '-'
                        )

                st.dataframe(result_data, use_container_width=True, height=500)
                st.caption(f"Menampilkan {len(result_data)} baris data")

            # Download buttons
            col_download1, col_download2 = st.columns(2)
            with col_download1:
                csv = result_data.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "hasil.csv")

            with col2:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result_data.to_excel(writer, index=False)

                st.download_button("Download Excel", output.getvalue(), "hasil.xlsx")
    
    # Tab 2: Input Teks
    with tab2:
        text = st.text_area(
            "Masukkan ulasan:",
            height=150,
            placeholder="Contoh: Materi yang diajarkan menarik dan mudah dipahami",
            help="Masukkan teks ulasan untuk dianalisis sentimen, indikator, dan keluhan"
        )
        
        analyze_button = st.button("🔍 Analisis NLP", key="btn_analisis_text", use_container_width=True)
        
        if analyze_button:
            if text and text.strip():
                if is_valid_text(text):
                    start_time = time.time()
                    with st.spinner("Menganalisis teks..."):
                        tokenizer_sent, model_sent = load_sentiment_model()
                        tokenizer_ind, model_ind = load_indikator_model()
                        tokenizer_kel, model_kel = load_keluhan_model()
                        label_map_ind = load_indikator_labels()
                        label_map_kel = load_keluhan_labels()
                        
                        sent_label, sent_conf = predict_sentiment(text, tokenizer_sent, model_sent)
                        ind_label, ind_conf = predict_indikator(text, tokenizer_ind, model_ind, label_map_ind)
                        kel_label, kel_conf = predict_keluhan(text, tokenizer_kel, model_kel, label_map_kel)
                        kel_label = validate_keluhan_with_indikator(ind_label, kel_label)
                    end_time = time.time()
                    processing_time = end_time - start_time
                    formatted_time = format_time(processing_time)
                    
                    color_map = {"Positif": "#28a745", "Netral": "#ffc107", "Negatif": "#dc3545"}
                    color = color_map.get(sent_label, "#0078d4")
                    emoji = "😊" if sent_label == "Positif" else "😐" if sent_label == "Netral" else "😞"
                        
                    st.markdown(f"""
                    <div style="padding:20px; background:linear-gradient(135deg, #0078d410, #00a8e810); border-radius:20px; margin-top:20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                            <h4 style="margin:0;">Hasil Analisis</h4>
                            <span class='info-badge' style="margin:0;">⏱️ {formatted_time}</span>
                        </div>
                        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:15px;">
                            <div style="text-align:center; padding:10px; background:rgba(0,0,0,0.08); border-radius:12px;">
                                <div style="font-size:0.9rem;">Sentimen</div>
                                <div style="font-size:1.6rem; font-weight:600; color:{color}">{sent_label} {emoji}</div>
                                <div style="font-size:0.9rem;">Confidence: {sent_conf:.2%}</div>
                            </div>
                            <div style="text-align:center; padding:10px; background:rgba(0,0,0,0.08); border-radius:12px;">
                                <div style="font-size:0.9rem;">Indikator</div>
                                <div style="font-size:1.2rem; font-weight:600;">{ind_label}</div>
                                <div style="font-size:0.9rem;">Confidence: {ind_conf:.2%}</div>
                            </div>
                            <div style="text-align:center; padding:10px; background:rgba(0,0,0,0.08); border-radius:12px;">
                                <div style="font-size:0.9rem;">Keluhan</div>
                                <div style="font-size:1.2rem; font-weight:600;">{kel_label}</div>
                                <div style="font-size:0.9rem;">Confidence: {kel_conf:.2%}</div>
                            </div>
                        </div>
                        <div style="margin-top:15px; font-style:italic; text-align:center; padding:12px; background:rgba(0,0,0,0.08); border-radius:12px;">
                            "{text}"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Teks tidak valid. Tambah kata-kata lainnya agar kalimat dapat dianalisis oleh sistem.")
            else:
                st.warning("⚠️ Silakan masukkan teks terlebih dahulu")