# EVALUASI LEVEL 1
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import URL_EVALUASI_L1, DAMPAK_ORDER, INDIKATOR_KELUHAN_MAP
from utils.helpers import (
    get_bar_color, 
    get_wordcloud_colormap, 
    color_sentiment, 
    sort_dampak, 
    process_text_for_wordcloud
)
from utils.styling import load_css

# Import INDIKATOR_KELUHAN_MAP
try:
    from utils.config import INDIKATOR_KELUHAN_MAP
except:
    INDIKATOR_KELUHAN_MAP = {}

# Load evaluasi L1 data from Google Sheet
def load_evaluasi_data():
    try:
        df = pd.read_csv(URL_EVALUASI_L1)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        df = df.replace('#NUM!', pd.NA)
        
        if 'Selesai' in df.columns:
            df['Selesai'] = pd.to_datetime(df['Selesai'], errors='coerce')
            df['Month-Year'] = df['Selesai'].dt.strftime('%b-%Y')
            df['Month-Year_Sort'] = df['Selesai'].dt.to_period('M')
        
        if 'Rata-rata Nilai Akumulasi' in df.columns:
            df['Rata-rata Nilai Akumulasi'] = pd.to_numeric(df['Rata-rata Nilai Akumulasi'], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()
    
# Render halaman Evaluasi L1
def render_evaluasi_l1():
    st.markdown("""
    <div class='page-header'>
        <h1 class='page-title'>💼 Dashboard Evaluasi Pembelajaran Level 1</h1>
        <p class='page-description'>Halaman ini Menyajikan Hasil Evaluasi Pembelajaran Level 1</p>
    </div>
    """, unsafe_allow_html=True)
    
    df_dashboard = load_evaluasi_data()
    
    if df_dashboard.empty:
        st.warning("Tidak ada data yang tersedia")
        return
    
    # Search filters
    col_search1, col_search2 = st.columns(2)
    with col_search1:
        search_title = st.text_input("🔍 Cari Judul Pembelajaran", placeholder="Masukkan judul pelatihan...")
    with col_search2:
        search_code = st.text_input("🔍 Cari Kode Judul", placeholder="Masukkan kode pelatihan...")
    
    # Filter dropdowns
    col_filter1, col_filter2, col_filter3, col_filter4, col_filter5, col_filter6 = st.columns(6)
    
    with col_filter1:
        if 'Month-Year' in df_dashboard.columns:
            month_year_labels = sorted(df_dashboard['Month-Year'].dropna().unique())
            selected_month = st.selectbox("Waktu", ["Semua"] + month_year_labels)
        else:
            selected_month = "Semua"
    
    with col_filter2:
        valid_indicators = df_dashboard["Indikator"].dropna().unique().tolist()
        selected_indicator = st.selectbox("Indikator", ["Semua"] + sorted(valid_indicators))
    
    with col_filter3:
        if selected_indicator != "Semua" and selected_indicator in INDIKATOR_KELUHAN_MAP:
            available_complaints = INDIKATOR_KELUHAN_MAP[selected_indicator]
            complaints_all = ["Semua"] + available_complaints
        else:
            valid_complaints = df_dashboard["Keluhan"].dropna().unique().tolist()
            complaints_all = ["Semua"] + sorted(valid_complaints)
        selected_complaint = st.selectbox("Keluhan", complaints_all)
    
    with col_filter4:
        valid_sentiments = df_dashboard["Sentimen"].dropna().unique().tolist()
        selected_sentiment = st.selectbox("Sentimen", ["Semua"] + sorted(valid_sentiments))
    
    with col_filter5:
        valid_impacts = df_dashboard["Dampak"].dropna().unique().tolist()
        valid_impacts_sorted = sort_dampak(valid_impacts)
        selected_impact = st.selectbox("Dampak", ["Semua"] + valid_impacts_sorted)
    
    with col_filter6:
        valid_tindak_lanjut = df_dashboard["Tindak Lanjut"].dropna().unique().tolist()
        selected_tindak_lanjut = st.selectbox("Tindak Lanjut", ["Semua"] + sorted(valid_tindak_lanjut))
    
    # Apply filters
    filtered_df = df_dashboard.copy()
    if search_title:
        filtered_df = filtered_df[filtered_df["Judul"].str.contains(search_title, case=False, na=False)]
    if search_code and 'Kode' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Kode"].str.contains(search_code, case=False, na=False)]
    if selected_month != "Semua":
        filtered_df = filtered_df[filtered_df['Month-Year'] == selected_month]
    if selected_indicator != "Semua":
        filtered_df = filtered_df[filtered_df["Indikator"] == selected_indicator]
    if selected_complaint != "Semua":
        filtered_df = filtered_df[filtered_df["Keluhan"] == selected_complaint]
    if selected_sentiment != "Semua":
        filtered_df = filtered_df[filtered_df["Sentimen"] == selected_sentiment]
    if selected_impact != "Semua":
        filtered_df = filtered_df[filtered_df["Dampak"] == selected_impact]
    if selected_tindak_lanjut != "Semua":
        filtered_df = filtered_df[filtered_df["Tindak Lanjut"] == selected_tindak_lanjut]
    
    # KPI Cards
    st.markdown("")
    st.markdown("<h5 style='margin-bottom: 5px;'>🎯 KPI Card</h5>", unsafe_allow_html=True)
    
    total_data = len(filtered_df)
    positive_count = len(filtered_df[filtered_df["Sentimen"] == "Positif"])
    neutral_count = len(filtered_df[filtered_df["Sentimen"] == "Netral"])
    negative_count = len(filtered_df[filtered_df["Sentimen"] == "Negatif"])
    
    positive_pct = (positive_count / total_data * 100) if total_data > 0 else 0
    neutral_pct = (neutral_count / total_data * 100) if total_data > 0 else 0
    negative_pct = (negative_count / total_data * 100) if total_data > 0 else 0
    
    col_score1, col_score2, col_score3, col_score4 = st.columns(4)
    
    with col_score1:
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value'>{total_data}</div>
            <div class='scorecard-label'>Jumlah Pembelajaran</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_score2:
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value' style='color: #28a745;'>{positive_pct:.1f}%</div>
            <div class='scorecard-label'>Feedback Positif</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_score3:
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value' style='color: #ffc107;'>{neutral_pct:.1f}%</div>
            <div class='scorecard-label'>Feedback Netral</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_score4:
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value' style='color: #dc3545;'>{negative_pct:.1f}%</div>
            <div class='scorecard-label'>Feedback Negatif</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    if not filtered_df.empty:
        col_chart1, col_chart2 = st.columns(2, gap="large")
        
        # Chart 1: Tren Sentimen per Bulan
        with col_chart1:
            st.markdown("<h5>📈 Tren Sentimen per Bulan</h5>", unsafe_allow_html=True)
            
            if 'Month-Year' in filtered_df.columns:
                unique_months = filtered_df[['Month-Year', 'Month-Year_Sort']].drop_duplicates()
                unique_months = unique_months.sort_values('Month-Year_Sort', ascending=False)
                last_12_months = unique_months.head(12)
                last_12_labels = last_12_months['Month-Year'].tolist()
                
                sentiment_by_month = filtered_df[filtered_df['Month-Year'].isin(last_12_labels)].groupby(['Month-Year', 'Sentimen']).size().reset_index(name='Jumlah')
                total_by_month = filtered_df[filtered_df['Month-Year'].isin(last_12_labels)].groupby('Month-Year').size().reset_index(name='Total')
                sentiment_by_month = sentiment_by_month.merge(total_by_month, on='Month-Year')
                sentiment_by_month['Persentase'] = (sentiment_by_month['Jumlah'] / sentiment_by_month['Total'] * 100).round(1)
                
                chart_months = sorted(last_12_months['Month-Year_Sort'].unique(), key=lambda x: x)
                chart_month_labels = [m.strftime('%b-%Y') for m in chart_months if pd.notna(m)]
                
                if not sentiment_by_month.empty:
                    chart = alt.Chart(sentiment_by_month).mark_bar(cornerRadius=4).encode(
                        x=alt.X('Month-Year:N', title='Periode', sort=chart_month_labels, axis=alt.Axis(labelAngle=-30)),
                        y=alt.Y('Jumlah:Q', title='Jumlah Feedback'),
                        color=alt.Color('Sentimen:N', scale=alt.Scale(
                            domain=['Positif', 'Netral', 'Negatif'],
                            range=['#28a745', '#ffc107', '#dc3545']
                        )),
                        tooltip=[
                            alt.Tooltip('Month-Year:N', title='Waktu'),
                            alt.Tooltip('Jumlah:Q', title='Jumlah Data'),
                            alt.Tooltip('Sentimen:N', title='Sentimen'),
                            alt.Tooltip('Persentase:Q', title='Persentase', format='.1f')
                        ]
                    ).properties(height=400)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("Tidak ada data untuk ditampilkan")
        
        # Chart 2: Distribusi Sentimen per Indikator
        with col_chart2:
            st.markdown("<h5>🚩 Distribusi Sentimen per Indikator</h5>", unsafe_allow_html=True)
            
            indicator_sentiment = filtered_df.groupby(['Indikator', 'Sentimen']).size().reset_index(name='Jumlah')
            total_by_indicator = filtered_df.groupby('Indikator').size().reset_index(name='Total')
            indicator_sentiment = indicator_sentiment.merge(total_by_indicator, on='Indikator')
            indicator_sentiment['Persentase'] = (indicator_sentiment['Jumlah'] / indicator_sentiment['Total'] * 100).round(1)
            
            if not indicator_sentiment.empty:
                chart = alt.Chart(indicator_sentiment).mark_bar(cornerRadius=4).encode(
                    x=alt.X('Jumlah:Q', title='Jumlah Feedback'),
                    y=alt.Y('Indikator:N', title=None, sort='-x'),
                    color=alt.Color('Sentimen:N', scale=alt.Scale(
                        domain=['Positif', 'Netral', 'Negatif'],
                        range=['#28a745', '#ffc107', '#dc3545']
                    )),
                    tooltip=[
                        alt.Tooltip('Indikator:N', title='Indikator'),
                        alt.Tooltip('Jumlah:Q', title='Jumlah Data'),
                        alt.Tooltip('Sentimen:N', title='Sentimen'),
                        alt.Tooltip('Persentase:Q', title='Persentase', format='.1f')
                    ]
                ).properties(height=400)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Tidak ada data untuk ditampilkan")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Chart 3: Heatmap Keluhan vs Dampak
        st.markdown(f"<h5>🔥 Jumlah Keluhan vs Dampak - {selected_sentiment if selected_sentiment != 'Semua' else 'Semua Sentimen'}</h5>", unsafe_allow_html=True)
        
        if 'Keluhan' in filtered_df.columns and 'Dampak' in filtered_df.columns:
            heatmap_data = pd.crosstab(filtered_df['Keluhan'], filtered_df['Dampak'])
            if not heatmap_data.empty:
                if selected_sentiment == "Positif":
                    colorscale = [[0, '#e8f5e9'], [0.2, '#c8e6c9'], [0.4, '#a5d6a7'], [0.6, '#81c784'], [0.8, '#66bb6a'], [1, '#2e7d32']]
                elif selected_sentiment == "Netral":
                    colorscale = [[0, '#fff8e1'], [0.2, '#ffecb3'], [0.4, '#ffe082'], [0.6, '#ffd54f'], [0.8, '#ffca28'], [1, '#ffa000']]
                elif selected_sentiment == "Negatif":
                    colorscale = [[0, '#ffebee'], [0.2, '#ffcdd2'], [0.4, '#ef9a9a'], [0.6, '#e57373'], [0.8, '#ef5350'], [1, '#d32f2f']]
                else:
                    colorscale = 'Blues'
                
                heatmap_data = heatmap_data[[col for col in DAMPAK_ORDER if col in heatmap_data.columns]]
                
                fig = px.imshow(
                    heatmap_data,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale=colorscale,
                    labels=dict(x="Dampak", y="Keluhan")
                )
                fig.update_layout(height=500, yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tidak ada data untuk ditampilkan")
        
        # Word Cloud and Top Words
        col_wc1, col_wc2 = st.columns(2, gap="large")
        
        with col_wc1:
            title_sentiment = selected_sentiment if selected_sentiment != "Semua" else "Semua Sentimen"
            st.markdown(f"<h5>🔝 Top 10 Kata Terbanyak - {title_sentiment}</h5>", unsafe_allow_html=True)
            
            if selected_sentiment != "Semua":
                text_df = filtered_df[filtered_df["Sentimen"] == selected_sentiment]
            else:
                text_df = filtered_df
            
            if 'Komentar' in text_df.columns and not text_df.empty:
                all_text = " ".join(text_df["Komentar"].astype(str))

                from utils.helpers import get_top_words, clean_text_for_words
                top_words = get_top_words(all_text, top_n=10, remove_stopwords=True)
                
                if top_words:
                    word_df = pd.DataFrame(top_words, columns=["Kata", "Frekuensi"])
                    
                    bar_color = get_bar_color(selected_sentiment)
                    chart = alt.Chart(word_df).mark_bar(cornerRadius=4, color=bar_color).encode(
                        x=alt.X("Frekuensi:Q", title="Frekuensi"),
                        y=alt.Y("Kata:N", sort="-x", title=None),
                        tooltip=["Kata", "Frekuensi"]
                    ).properties(height=350)
                    
                    text = chart.mark_text(
                        align='left',
                        baseline='middle',
                        dx=5,
                        fontSize=11,
                        fontWeight=600,
                        color=bar_color
                    ).encode(text='Frekuensi:Q')
                    
                    st.altair_chart(chart + text, use_container_width=True)
                else:
                    st.info(f"Tidak cukup data untuk top kata pada sentimen {title_sentiment}")
            else:
                st.info("Tidak ada data komentar")
        
        with col_wc2:
            st.markdown(f"<h5>☁️ Word Cloud - {title_sentiment}</h5>", unsafe_allow_html=True)
            
            if selected_sentiment != "Semua":
                text_df = filtered_df[filtered_df["Sentimen"] == selected_sentiment]
            else:
                text_df = filtered_df
            
            if 'Komentar' in text_df.columns and not text_df.empty:
                all_text = " ".join(text_df["Komentar"].astype(str))
                processed_text = process_text_for_wordcloud(all_text)
                
                if processed_text and len(processed_text.split()) > 10:
                    wc_colormap = get_wordcloud_colormap(selected_sentiment)
                    
                    fig, ax = plt.subplots(figsize=(8, 4))
                    fig.patch.set_alpha(0)
                    ax.patch.set_alpha(0)
                    
                    wc = WordCloud(
                        width=800, height=450, background_color=None, mode='RGBA',
                        colormap=wc_colormap, max_words=50, contour_width=1, random_state=42
                    ).generate(processed_text)
                    
                    ax.imshow(wc, interpolation='bilinear')
                    ax.axis('off')
                    plt.tight_layout(pad=0)
                    
                    st.pyplot(fig, use_container_width=True)
                else:
                    st.info(f"Tidak cukup data untuk word cloud pada sentimen {title_sentiment}")
    
    # Data Table
    st.markdown("<h5 style='margin-bottom: 15px;'>📋 Detail Data Evaluasi Level 1</h5>", unsafe_allow_html=True)
    if not filtered_df.empty:
        display_columns = [
            'Kode', 'Judul', 'Mulai', 'Selesai', 'Penyelenggaraan', 'Indikator', 
            'Komentar', 'Rata-rata Nilai Akumulasi', 'Bulan', 'PIC', 'Pemetaan', 
            'Keluhan', 'Sentimen', 'Kemungkinan', 'Dampak', 'Tindak Lanjut', 
            'Rencana Perlakuan', 'Status', 'Keterangan (plus Evidence)'
        ]
        
        available_columns = [col for col in display_columns if col in filtered_df.columns]
        display_df = filtered_df[available_columns].copy()
        
        if 'Mulai' in display_df.columns:
            display_df['Mulai'] = pd.to_datetime(display_df['Mulai'], errors='coerce').dt.strftime('%Y-%m-%d')
        if 'Selesai' in display_df.columns:
            display_df['Selesai'] = pd.to_datetime(display_df['Selesai'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        styled_df = display_df.style
        if "Sentimen" in display_df.columns:
            styled_df = styled_df.map(color_sentiment, subset=["Sentimen"])
        
        st.dataframe(styled_df, use_container_width=True, height=500)
        st.caption(f"Menampilkan {len(display_df)} baris data")
        
        # Download buttons
        col_download1, col_download2 = st.columns(2)
        download_df = filtered_df[available_columns].copy()
        
        with col_download1:
            csv = download_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"dashboard_l1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_download2:
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                download_df.to_excel(writer, index=False, sheet_name='Dashboard L1')
            excel_data = output.getvalue()
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name=f"dashboard_l1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.info("Tidak ada data yang sesuai dengan filter yang dipilih")