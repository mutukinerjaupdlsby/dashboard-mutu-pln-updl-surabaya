# SISTEM NLP
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import time
from datetime import datetime
import numpy as np
import plotly.express as px

# Import models
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    load_sentiment_model, predict_sentiment,
    load_indikator_model, load_indikator_labels, predict_indikator,
    load_keluhan_model, load_keluhan_labels, predict_keluhan, validate_keluhan_with_indikator
)
from utils.config import INDIKATOR_KELUHAN_MAP
from utils.helpers import format_time, is_valid_text, get_bar_color, get_wordcloud_colormap, color_sentiment, process_text_for_wordcloud

# Memproses dataframe dengan model NLP
def process_data_nlp(df):
    start_time = time.time()
    
    # Load models
    tokenizer_sent, model_sent = load_sentiment_model()
    tokenizer_ind, model_ind = load_indikator_model()
    tokenizer_kel, model_kel = load_keluhan_model()
    label_map_ind = load_indikator_labels()
    label_map_kel = load_keluhan_labels()
    
    labels = []
    confidences = []
    indikator_labels = []
    indikator_confs = []
    keluhan_labels = []
    keluhan_confs = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, text in enumerate(df["Komentar"]):
        if is_valid_text(text):
            sent_label, sent_conf = predict_sentiment(str(text), tokenizer_sent, model_sent)
            labels.append(sent_label)
            confidences.append(sent_conf)
            
            ind_label, ind_conf = predict_indikator(str(text), tokenizer_ind, model_ind, label_map_ind)
            indikator_labels.append(ind_label)
            indikator_confs.append(ind_conf)
            
            kel_label, kel_conf = predict_keluhan(str(text), tokenizer_kel, model_kel, label_map_kel)
            kel_label = validate_keluhan_with_indikator(ind_label, kel_label)
            keluhan_labels.append(kel_label)
            keluhan_confs.append(kel_conf)
        else:
            labels.append("Invalid")
            confidences.append(None)
            indikator_labels.append("Invalid")
            indikator_confs.append(None)
            keluhan_labels.append("Invalid")
            keluhan_confs.append(None)
        
        progress = (i + 1) / len(df)
        progress_bar.progress(progress)
        status_text.text(f"Memproses data ke-{i+1} dari {len(df)}")
    
    df["Sentimen"] = labels
    df["Confidence"] = confidences
    df["Indikator"] = indikator_labels
    df["Indikator Confidence"] = indikator_confs
    df["Keluhan"] = keluhan_labels
    df["Keluhan Confidence"] = keluhan_confs
    
    progress_bar.empty()
    status_text.empty()
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    st.session_state.df = df
    st.session_state.processing_time = processing_time
    st.session_state.analysis_done = True

# Render halaman Sistem NLP
def render_sistem_nlp():
    st.markdown("""
    <div class='page-header'>
        <h1 class='page-title'>💬 Sistem NLP</h1>
        <p class='page-description'>Analisis Sentimen, Indikator, dan Keluhan Secara Otomatis Menggunakan AI untuk Evaluasi Feedback Peserta Pembelajaran</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📁 Import File", "📝 Input Teks"])
    
    # Tab 1: Import File
    with tab1:
        uploaded = st.file_uploader(
            "Upload file CSV / XLS / XLSX",
            type=["csv", "xls", "xlsx"],
            help="File harus memiliki kolom 'Komentar' untuk dianalisis"
        )
        
        if uploaded is None:
            st.session_state.pop("analysis_done", None)
            st.session_state.pop("df", None)
            st.session_state.pop("processing_time", None)
        
        if uploaded:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            st.markdown("##### 📄 Preview Data")
            st.dataframe(df.head(10), use_container_width=True)
            st.markdown(f"**Total Data:** {len(df)} baris")
            
            if "Komentar" not in df.columns:
                st.error("❌ Dataset harus memiliki kolom 'Komentar'")
            else:
                if st.button("🔍 Analisis NLP", key="btn_analisis_dataset", use_container_width=True):
                    process_data_nlp(df)
                    st.rerun()
        
        # Display results
        if "analysis_done" in st.session_state and st.session_state.analysis_done and "df" in st.session_state:
            df = st.session_state.df
            processing_time = st.session_state.processing_time
            formatted_time = format_time(processing_time)
            
            df_valid = df[df["Sentimen"] != "Invalid"].copy()
            invalid_count = len(df) - len(df_valid)
            
            total = len(df_valid)
            pos = len(df_valid[df_valid["Sentimen"] == "Positif"])
            neu = len(df_valid[df_valid["Sentimen"] == "Netral"])
            neg = len(df_valid[df_valid["Sentimen"] == "Negatif"])
            
            pos_ratio = pos / total * 100 if total > 0 else 0
            neu_ratio = neu / total * 100 if total > 0 else 0
            neg_ratio = neg / total * 100 if total > 0 else 0
            
            sentiment_counts = df_valid["Sentimen"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentimen", "Jumlah"]
            sentiment_counts["Persen"] = sentiment_counts["Jumlah"] / total * 100 if total > 0 else 0
            
            st.markdown(f"""
            <div class='info-badge'>
                ⏱️ Waktu proses: {formatted_time}
            </div>
            """, unsafe_allow_html=True)
            
            if invalid_count > 0:
                st.warning(f"⚠️ {invalid_count} data tidak valid sehingga tidak dianalisis oleh sistem.")
            
            st.markdown(f"""
            <div class='metric-container' style='margin: 60px 0 60px 0px;'>
                <div class='metric-item'>
                    <div class='metric-value'>{total}</div>
                    <div class='metric-label'>Total Ulasan Valid</div>
                </div>
                <div class='metric-item'>
                    <div class='metric-value' style='color: #28a745;'>{pos}</div>
                    <div class='metric-label'>Positif ({pos_ratio:.1f}%)</div>
                </div>
                <div class='metric-item'>
                    <div class='metric-value' style='color: #ffc107;'>{neu}</div>
                    <div class='metric-label'>Netral ({neu_ratio:.1f}%)</div>
                </div>
                <div class='metric-item'>
                    <div class='metric-value' style='color: #dc3545;'>{neg}</div>
                    <div class='metric-label'>Negatif ({neg_ratio:.1f}%)</div>
                </div>
                <div class='metric-item'>
                    <div class='metric-value' style='color: #6c757d;'>{invalid_count}</div>
                    <div class='metric-label'>Data Invalid</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if total > 0:
                col1, col2 = st.columns(2, gap="large")
                
                with col1:
                    st.markdown(f"<h5>🎭 Distribusi Sentimen</h5>", unsafe_allow_html=True)
                    bar_chart = alt.Chart(sentiment_counts).mark_bar(cornerRadius=5, size=90).encode(
                        x=alt.X('Sentimen:N', axis=alt.Axis(labelAngle=0, title=None)),
                        y=alt.Y('Jumlah:Q', title='Jumlah'),
                        color=alt.Color('Sentimen:N', scale=alt.Scale(
                            domain=['Positif', 'Netral', 'Negatif'],
                            range=['#28a745', '#ffc107', '#dc3545']
                        )),
                        tooltip=['Sentimen', 'Jumlah']
                    )
                    text = bar_chart.mark_text(align='center', baseline='bottom', dy=-5, fontSize=12, fontWeight=600).encode(text='Jumlah:Q')
                    st.altair_chart(bar_chart + text, use_container_width=True)
                
                with col2:
                    st.markdown(f"<h5>🥧 Persentase Sentimen</h5>", unsafe_allow_html=True)
                    pie_chart = alt.Chart(sentiment_counts).mark_arc(cornerRadius=4, outerRadius=125).encode(
                        theta=alt.Theta(field='Jumlah', type='quantitative'),
                        color=alt.Color('Sentimen:N', scale=alt.Scale(
                            domain=['Positif', 'Netral', 'Negatif'],
                            range=['#28a745', '#ffc107', '#dc3545']
                        )),
                        tooltip=['Sentimen:N', alt.Tooltip('Jumlah:Q', title='Jumlah'), alt.Tooltip('Persen:Q', format='.2f', title='Persentase %')]
                    )
                    text = pie_chart.mark_text(radius=140, size=12, fontWeight=600).encode(text=alt.Text('Persen:Q', format='.2f'))
                    st.altair_chart(pie_chart + text, use_container_width=True)
                
                col_ind, col_kel = st.columns(2)
                    
                with col_ind:
                    st.markdown("<h5>🚩 Distribusi Indikator</h5>", unsafe_allow_html=True)
                    if not df_valid.empty and 'Indikator' in df_valid.columns:
                        ind_data = df_valid.groupby(['Indikator', 'Sentimen']).size().reset_index(name='Jumlah')
                        total_per_ind = df_valid.groupby('Indikator').size().reset_index(name='Total')
                        ind_data = ind_data.merge(total_per_ind, on='Indikator')
                        ind_data['Persentase'] = (ind_data['Jumlah'] / ind_data['Total'] * 100).round(1)
                        
                        ind_order = total_per_ind.sort_values('Total', ascending=True)['Indikator'].tolist()
                        
                        fig_ind = px.bar(
                            ind_data,
                            x='Jumlah',
                            y='Indikator',
                            color='Sentimen',
                            orientation='h',
                            text='Jumlah',
                            color_discrete_map={
                                'Positif': '#28a745',
                                'Netral': '#ffc107',
                                'Negatif': '#dc3545'
                            },
                            title=None,
                            height=500
                        )
                        
                        fig_ind.update_layout(
                            yaxis={'categoryorder': 'array', 'categoryarray': ind_order},
                            xaxis_title="Jumlah Feedback",
                            yaxis_title=None,
                            bargap=0.2,
                            hovermode='closest',
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            height=500,
                            hoverlabel=dict(
                                bgcolor="white",
                                font_size=12,
                                font_family="Arial",
                                bordercolor="rgba(0,0,0,0.2)"
                            )
                        )
                        
                        fig_ind.update_traces(
                            textposition='outside',
                            texttemplate='%{text}',
                            hovertemplate='<b>%{y}</b><br>' +
                                        'Jumlah: %{x}<br>' +
                                        'Sentimen: %{fullData.name}<br>' +
                                        'Persentase: %{customdata[0]}%<extra></extra>',
                            customdata=ind_data[['Persentase']].values
                        )
                        
                        st.markdown("""<div style="overflow-y: auto; max-height: 600px;">""", unsafe_allow_html=True) 
                        st.plotly_chart(fig_ind, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    else:
                        st.info("Tidak ada data indikator untuk ditampilkan.")
                    
                with col_kel:
                    st.markdown("<h5>🔥 Distribusi Keluhan</h5>", unsafe_allow_html=True)
                    if not df_valid.empty and 'Keluhan' in df_valid.columns:
                        kel_data = df_valid.groupby(['Keluhan', 'Sentimen']).size().reset_index(name='Jumlah')
                        total_per_kel = df_valid.groupby('Keluhan').size().reset_index(name='Total')
                        kel_data = kel_data.merge(total_per_kel, on='Keluhan')
                        kel_data['Persentase'] = (kel_data['Jumlah'] / kel_data['Total'] * 100).round(1)
                        
                        kel_order = total_per_kel.sort_values('Total', ascending=True)['Keluhan'].tolist()
                        
                        fig_kel = px.bar(
                            kel_data,
                            x='Jumlah',
                            y='Keluhan',
                            color='Sentimen',
                            orientation='h',
                            text='Jumlah',
                            color_discrete_map={
                                'Positif': '#28a745',
                                'Netral': '#ffc107',
                                'Negatif': '#dc3545'
                            },
                            title=None,
                            height=500
                        )
                        
                        fig_kel.update_layout(
                            yaxis={'categoryorder': 'array', 'categoryarray': kel_order},
                            xaxis_title="Jumlah Feedback",
                            yaxis_title=None,
                            bargap=0.2,
                            hovermode='closest',  # Diubah dari 'y unified' menjadi 'closest'
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            height=500,
                            hoverlabel=dict(
                                bgcolor="white",
                                font_size=12,
                                font_family="Arial",
                                bordercolor="rgba(0,0,0,0.2)"
                            )
                        )
                        
                        fig_kel.update_traces(
                            textposition='outside',
                            texttemplate='%{text}',
                            hovertemplate='<b>%{y}</b><br>' +
                                        'Jumlah: %{x}<br>' +
                                        'Sentimen: %{fullData.name}<br>' +
                                        'Persentase: %{customdata[0]}%<extra></extra>',
                            customdata=kel_data[['Persentase']].values
                        )
                        
                        st.markdown("""<div style="overflow-y: auto; max-height: 600px;">""", unsafe_allow_html=True)
                        st.plotly_chart(fig_kel, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    else:
                        st.info("Tidak ada data keluhan untuk ditampilkan.")
                
                dominant = df_valid["Sentimen"].value_counts().idxmax() if total > 0 else "Tidak Ada"
                avg_confidence = df_valid["Confidence"].mean() if total > 0 else 0
                
                st.markdown("<h5 style='margin-top:30px;'>📈 Summary</h5>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(0,120,212,0.05), rgba(0,168,232,0.05)); padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid rgba(0,120,212,0.2);'>
                    <ul style='line-height: 2;'>
                        <li><b>Total Data Valid:</b> {total} ulasan</li>
                        <li><b>Data Invalid:</b> {invalid_count} ulasan</li>
                        <li><b>Distribusi:</b> 
                            <span style='color: #28a745;'>Positif ({pos}) ({pos_ratio:.1f}%)</span> | 
                            <span style='color: #ffc107;'>Netral ({neu}) ({neu_ratio:.1f}%)</span> | 
                            <span style='color: #dc3545;'>Negatif ({neg}) ({neg_ratio:.1f}%)</span>
                        </li>
                        <li><b>Sentimen Dominan:</b> <span style='color: #0078d4; font-weight: 600;'>{dominant}</span></li>
                        <li><b>Rata-rata Confidence:</b> {avg_confidence:.2%}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # Data table
            st.markdown(f"<h5 style='margin-top:30px'>📋 Detail Data Hasil Sistem NLP</h5>", unsafe_allow_html=True)
            result_data = df.copy()
            for col_conf in ['Confidence', 'Indikator Confidence', 'Keluhan Confidence']:
                if col_conf in result_data.columns:
                    result_data[col_conf] = result_data[col_conf].apply(lambda x: f"{x:.2%}" if isinstance(x, (int, float)) and pd.notna(x) else '-')
            
            styled_df = result_data.style.map(color_sentiment, subset=['Sentimen'])
            st.dataframe(styled_df, use_container_width=True, height=500)
            st.caption(f"Menampilkan {len(result_data)} baris data")
            
            # Download buttons
            col_download1, col_download2 = st.columns(2)
            with col_download1:
                csv = result_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"hasil_nlp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_download2:
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result_data.to_excel(writer, index=False, sheet_name='Hasil Analisis NLP')
                excel_data = output.getvalue()
                st.download_button(
                    label="📥 Download XLSX",
                    data=excel_data,
                    file_name=f"hasil_nlp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
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