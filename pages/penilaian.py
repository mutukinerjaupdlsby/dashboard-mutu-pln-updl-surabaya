# PENILAIAN
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import URL_PENILAIAN
from utils.helpers import color_nilai, format_angka

# Load penilaian data from Google Shee
def load_penilaian_data():
    try:
        df = pd.read_csv(URL_PENILAIAN)
        df.columns = df.columns.str.replace('\ufeff', '').str.strip()
        
        numeric_columns = [
            'P.Isi', 'P.Hadir', 
            'Ins-Eng-1 of 2', 'Ins-Eng-2 of 2', 'Ins-Rel-1 of 2', 'Ins-Rel-2 of 2',
            'Ins-Sat-1 of 4', 'Ins-Sat-2 of 4', 'Ins-Sat-3 of 4', 'Ins-Sat-4 of 4',
            'Ins-Rat', 'Ins-Val',
            'Mat-Eng-1 of 2', 'Mat-Eng-2 of 2', 'Mat-Rel-1 of 2', 'Mat-Rel-2 of 2',
            'Mat-Sat-1 0f 2', 'Mat-Sat-2 of 2', 'Mat-Rat', 'Mat-Val',
            'Sarpras-Sas-1 of 5', 'Sarpras-Sas-2 of 5', 'Sarpras-Sas-3 of 5',
            'Sarpras-Sas-4 of 5', 'Sarpras-Sas-5 of 5', 'Sarpras-Rat',
            'Dig-Sas-1 of 5', 'Dig-Sas-2 of 5', 'Dig-Sas-3 of 5',
            'Dig-Sas-4 of 5', 'Dig-Sas-5 of 5', 'Dig Rat'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        categorical_columns = ['Kode Judul', 'Judul Pembelajaran', 'Bidang', 'Angkatan', 'UPDL Penyelenggara', 'Jenis Diklat', 'Strategi Pelaksana']
        for col in categorical_columns:
            if col in df.columns:
                df[col] = df[col].fillna('').astype(str)
        
        if 'Rata-rata Nilai' not in df.columns:
            available_ratings = []
            for col in ['Ins-Rat', 'Mat-Rat', 'Sarpras-Rat', 'Dig Rat']:
                if col in df.columns:
                    available_ratings.append(col)
            
            if available_ratings:
                df['Rata-rata Nilai'] = df[available_ratings].mean(axis=1)
            else:
                df['Rata-rata Nilai'] = np.nan
        
        if 'Tgl Mulai' in df.columns:
            df['Tgl Mulai'] = pd.to_datetime(df['Tgl Mulai'], errors='coerce')
            df['Month-Year'] = df['Tgl Mulai'].dt.strftime('%b-%Y')
            df['Month-Year_Sort'] = df['Tgl Mulai'].dt.to_period('M')
        else:
            df['Month-Year'] = 'Jan-2024'
            df['Month-Year_Sort'] = pd.Period('2024-01')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# render halaman penilaian
def render_penilaian():
    st.markdown("""
    <div class='page-header'>
        <h1 class='page-title'>🏆 Dashboard Penilaian Pembelajaran</h1>
        <p class='page-description'>Halaman ini menyajikan lengkap hasil penilaian peserta pembelajaran</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_penilaian_data()
    
    if df.empty:
        st.warning("Tidak ada data untuk divisualisasikan saat ini. Silakan periksa koneksi Google Sheet.")
        return
    
    # Search inputs
    col_search1, col_search2 = st.columns(2)
    with col_search1:
        search_title = st.text_input("🔍 Cari Judul Pembelajaran", placeholder="Masukkan judul...")
    with col_search2:
        search_code = st.text_input("🔍 Cari Kode Judul", placeholder="Masukkan kode...")
    
    # Filters
    col_filter1, col_filter2, col_filter3, col_filter4, col_filter5 = st.columns(5)
    
    month_year_labels = sorted(df['Month-Year'].dropna().unique()) if len(df) > 0 else []
    
    with col_filter1:
        month_year_filter = st.selectbox("Waktu", ["Semua"] + month_year_labels)
    
    with col_filter2:
        penyelenggara_values = df['UPDL Penyelenggara'].replace('', 'Tidak Terisi').unique().tolist()
        penyelenggara_options = ["Semua"] + sorted([str(x) for x in penyelenggara_values if str(x) != ''])
        penyelenggara_filter = st.selectbox("Penyelenggara", penyelenggara_options)
    
    with col_filter3:
        angkatan_values = df['Angkatan'].replace('', 'Tidak Terisi').unique().tolist()
        angkatan_numeric = []
        angkatan_text = []
        for x in angkatan_values:
            if str(x) != 'Tidak Terisi' and str(x) != '':
                try:
                    angkatan_numeric.append(int(float(x)))
                except:
                    angkatan_text.append(str(x))
            else:
                angkatan_text.append('Tidak Terisi')
        
        angkatan_numeric_sorted = sorted(angkatan_numeric)
        angkatan_sorted = [str(a) for a in angkatan_numeric_sorted] + sorted(angkatan_text)
        angkatan_options = ["Semua"] + angkatan_sorted
        angkatan_filter = st.selectbox("Angkatan", angkatan_options)
    
    with col_filter4:
        jenis_diklat_values = df['Jenis Diklat'].replace('', 'Tidak Terisi').unique().tolist()
        jenis_diklat_options = ["Semua"] + sorted([str(x) for x in jenis_diklat_values if str(x) != ''])
        jenis_diklat_filter = st.selectbox("Jenis Diklat", jenis_diklat_options)
    
    with col_filter5:
        strategi_values = df['Strategi Pelaksana'].replace('', 'Tidak Terisi').unique().tolist()
        strategi_options = ["Semua"] + sorted([str(x) for x in strategi_values if str(x) != ''])
        strategi_filter = st.selectbox("Strategi Pelaksana", strategi_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    if month_year_filter != "Semua":
        filtered_df = filtered_df[filtered_df['Month-Year'] == month_year_filter]
    if penyelenggara_filter != "Semua":
        if penyelenggara_filter == "Tidak Terisi":
            filtered_df = filtered_df[filtered_df['UPDL Penyelenggara'] == '']
        else:
            filtered_df = filtered_df[filtered_df['UPDL Penyelenggara'] == penyelenggara_filter]
    if angkatan_filter != "Semua":
        if angkatan_filter == "Tidak Terisi":
            filtered_df = filtered_df[filtered_df['Angkatan'] == '']
        else:
            filtered_df = filtered_df[filtered_df['Angkatan'] == angkatan_filter]
    if jenis_diklat_filter != "Semua":
        if jenis_diklat_filter == "Tidak Terisi":
            filtered_df = filtered_df[filtered_df['Jenis Diklat'] == '']
        else:
            filtered_df = filtered_df[filtered_df['Jenis Diklat'] == jenis_diklat_filter]
    if strategi_filter != "Semua":
        if strategi_filter == "Tidak Terisi":
            filtered_df = filtered_df[filtered_df['Strategi Pelaksana'] == '']
        else:
            filtered_df = filtered_df[filtered_df['Strategi Pelaksana'] == strategi_filter]
    if search_title:
        filtered_df = filtered_df[filtered_df['Judul Pembelajaran'].str.contains(search_title, case=False, na=False)]
    if search_code:
        filtered_df = filtered_df[filtered_df['Kode Judul'].str.contains(search_code, case=False, na=False)]
    
    if filtered_df.empty:
        st.warning("Tidak ada data dengan filter yang dipilih.")
        return
    
    # KPI Cards
    st.markdown("<h5>🎯 KPI Card</h5>", unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)
    
    with col_m1:
        total_training = len(filtered_df)
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value'>{total_training}</div>
            <div class='scorecard-label'>Total Pelatihan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        avg_nilai = filtered_df['Rata-rata Nilai'].mean()
        nilai_display = f"{avg_nilai:.2f}" if pd.notna(avg_nilai) else "N/A"
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value'>{nilai_display}</div>
            <div class='scorecard-label'>Rata-rata Nilai</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m3:
        if 'Ins-Rat' in filtered_df.columns:
            avg_ins = pd.to_numeric(filtered_df['Ins-Rat'], errors='coerce').mean()
            ins_display = f"{avg_ins:.2f}" if pd.notna(avg_ins) else "N/A"
        else:
            ins_display = "N/A"
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value'>{ins_display}</div>
            <div class='scorecard-label'>Rata-rata Instruktur</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m4:
        if 'Mat-Rat' in filtered_df.columns:
            avg_mat = pd.to_numeric(filtered_df['Mat-Rat'], errors='coerce').mean()
            mat_display = f"{avg_mat:.2f}" if pd.notna(avg_mat) else "N/A"
        else:
            mat_display = "N/A"
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value'>{mat_display}</div>
            <div class='scorecard-label'>Rata-rata Materi</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m5:
        if 'Sarpras-Rat' in filtered_df.columns:
            avg_sarpras = pd.to_numeric(filtered_df['Sarpras-Rat'], errors='coerce').mean()
            sarpras_display = f"{avg_sarpras:.2f}" if pd.notna(avg_sarpras) else "N/A"
        else:
            sarpras_display = "N/A"
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value'>{sarpras_display}</div>
            <div class='scorecard-label'>Rata-rata Sarpras</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m6:
        if 'Dig Rat' in filtered_df.columns:
            avg_dig = pd.to_numeric(filtered_df['Dig Rat'], errors='coerce').mean()
            dig_display = f"{avg_dig:.2f}" if pd.notna(avg_dig) else "N/A"
        else:
            dig_display = "N/A"
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value'>{dig_display}</div>
            <div class='scorecard-label'>Rata-rata Digital</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col_viz1, col_viz2 = st.columns(2)
    chart_bg = 'rgba(0,0,0,0)'
    
    with col_viz1:
        # Trend chart
        if 'Month-Year_Sort' in filtered_df.columns:
            trend_data = filtered_df.groupby('Month-Year_Sort')['Rata-rata Nilai'].mean().reset_index()
            trend_data = trend_data.sort_values('Month-Year_Sort').tail(12)
            trend_data['Month_Year_Str'] = trend_data['Month-Year_Sort'].dt.strftime('%b-%Y')
            
            fig_trend = px.line(
                trend_data,
                x='Month_Year_Str',
                y='Rata-rata Nilai',
                markers=True,
                text=trend_data['Rata-rata Nilai'].apply(lambda x: f"{x:.2f}"),
                title="📈 Tren Rata-rata Nilai"
            )
            fig_trend.update_traces(
                textposition='top center',
                line=dict(color='#0078d4', width=2),
                marker=dict(size=8, color='#0078d4')
            )
            fig_trend.update_layout(
                plot_bgcolor=chart_bg,
                paper_bgcolor=chart_bg,
                xaxis_title="Periode (Bulan-Tahun)",
                yaxis_title="Rata-rata Nilai",
                xaxis=dict(gridcolor='rgba(128,128,128,0.1)', tickangle=-30),
                yaxis=dict(gridcolor='rgba(128,128,128,0.1)', range=[1, 5]),
                height=400
            )
            st.plotly_chart(fig_trend, use_container_width=True)
    
    with col_viz2:
        # Distribution chart
        filtered_df['Nilai_Kategori'] = pd.cut(
            filtered_df['Rata-rata Nilai'],
            bins=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
            labels=['0-0.5', '0.5-1', '1-1.5', '1.5-2', '2-2.5', '2.5-3', '3-3.5', '3.5-4', '4-4.5', '4.5-5'],
            right=False,
            include_lowest=True
        )
        
        kategori_counts = filtered_df['Nilai_Kategori'].value_counts().reset_index()
        kategori_counts.columns = ['Kategori', 'Frekuensi']
        kategori_counts = kategori_counts.sort_values('Kategori')
        
        fig_dist = px.bar(
            kategori_counts,
            x='Kategori',
            y='Frekuensi',
            title="📊 Distribusi Nilai Pelatihan",
            text='Frekuensi',
            color_discrete_sequence=['#00a8e8']
        )
        fig_dist.update_traces(textposition='outside', textfont=dict(size=12, color='#00a8e8'))
        fig_dist.update_layout(
            plot_bgcolor=chart_bg,
            paper_bgcolor=chart_bg,
            xaxis_title="Kategori Nilai",
            yaxis_title="Frekuensi",
            xaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
            yaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
            height=400
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    col_viz3, col_viz4 = st.columns(2)
    
    with col_viz3:
        # Nilai per Jenis Diklat
        jenis_perf = filtered_df.groupby('Jenis Diklat')['Rata-rata Nilai'].mean().reset_index()
        jenis_perf = jenis_perf[jenis_perf['Jenis Diklat'] != '']
        jenis_perf = jenis_perf.sort_values('Rata-rata Nilai', ascending=False)
        
        if not jenis_perf.empty:
            fig_jenis = px.bar(
                jenis_perf,
                x='Jenis Diklat',
                y='Rata-rata Nilai',
                text=jenis_perf['Rata-rata Nilai'].apply(lambda x: f"{x:.2f}"),
                title="📚 Rata-rata Nilai per Jenis Diklat",
                color_discrete_sequence=['#2c7da0']
            )
            fig_jenis.update_traces(
                textposition='outside',
                textfont=dict(size=11),
                marker=dict(color='#2c7da0', line=dict(color='#1f5068', width=1))
            )
            fig_jenis.update_layout(
                plot_bgcolor=chart_bg,
                paper_bgcolor=chart_bg,
                xaxis_title="Jenis Diklat",
                yaxis_title="Rata-rata Nilai (1-5)",
                xaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
                yaxis=dict(gridcolor='rgba(128,128,128,0.1)', range=[1, 5.5]),
                height=400
            )
            st.plotly_chart(fig_jenis, use_container_width=True)
    
    with col_viz4:
        # Nilai per Strategi Pelaksana
        strategi_perf = filtered_df.groupby('Strategi Pelaksana')['Rata-rata Nilai'].mean().reset_index()
        strategi_perf = strategi_perf[strategi_perf['Strategi Pelaksana'] != '']
        strategi_perf = strategi_perf.sort_values('Rata-rata Nilai', ascending=False)
        
        if not strategi_perf.empty:
            fig_strategi = px.bar(
                strategi_perf,
                x='Strategi Pelaksana',
                y='Rata-rata Nilai',
                text=strategi_perf['Rata-rata Nilai'].apply(lambda x: f"{x:.2f}"),
                title="🎯 Rata-rata Nilai per Strategi Pelaksana",
                color_discrete_sequence=['#1f5068']
            )
            fig_strategi.update_traces(
                textposition='outside',
                textfont=dict(size=11),
                marker=dict(color='#1f5068', line=dict(color='#0e2a38', width=1))
            )
            fig_strategi.update_layout(
                plot_bgcolor=chart_bg,
                paper_bgcolor=chart_bg,
                xaxis_title="Strategi Pelaksana",
                yaxis_title="Rata-rata Nilai (1-5)",
                xaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
                yaxis=dict(gridcolor='rgba(128,128,128,0.1)', range=[1, 5.5]),
                height=400
            )
            st.plotly_chart(fig_strategi, use_container_width=True)
    
    # Data Table
    st.markdown("<h5 style='margin: 40px 0 20px 0;'>📋 Detail Data Penilaian</h5>", unsafe_allow_html=True)
    
    display_columns = [col for col in filtered_df.columns if col not in ['Month-Year', 'Month_Year', 'Month-Year_Sort', 'Nilai_Kategori']]
    display_df = filtered_df[display_columns].copy()
    
    def format_numeric_columns(df):
        for col in df.columns:
            if df[col].dtype in ['float64', 'float32']:
                if col in ['P.Isi', 'P.Hadir']:
                    df[col] = df[col].apply(lambda x: f"{int(x)}" if pd.notna(x) else '-')
                else:
                    df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else '-')
            elif df[col].dtype in ['int64', 'int32']:
                df[col] = df[col].apply(lambda x: f"{x}" if pd.notna(x) else '-')
        return df
    
    display_df = format_numeric_columns(display_df)
    
    def color_rating(val):
        try:
            if isinstance(val, str) and val != '-':
                numeric_val = float(val)
                if numeric_val >= 4.5:
                    return 'background-color: #28a74530; color: #155724; font-weight: bold'
                elif numeric_val >= 4.0:
                    return 'background-color: #28a74520; color: #28a745'
                elif numeric_val >= 3.5:
                    return 'background-color: #ffc10720; color: #ffc107'
                elif numeric_val >= 3.0:
                    return 'background-color: #fd7e1420; color: #fd7e14'
                else:
                    return 'background-color: #dc354520; color: #dc3545'
        except:
            pass
        return ''
    
    rating_columns = [
        'Ins-Eng-1 of 2', 'Ins-Eng-2 of 2', 'Ins-Rel-1 of 2', 'Ins-Rel-2 of 2',
        'Ins-Sat-1 of 4', 'Ins-Sat-2 of 4', 'Ins-Sat-3 of 4', 'Ins-Sat-4 of 4',
        'Ins-Rat', 'Ins-Val',
        'Mat-Eng-1 of 2', 'Mat-Eng-2 of 2', 'Mat-Rel-1 of 2', 'Mat-Rel-2 of 2',
        'Mat-Sat-1 0f 2', 'Mat-Sat-2 of 2', 'Mat-Rat', 'Mat-Val',
        'Sarpras-Sas-1 of 5', 'Sarpras-Sas-2 of 5', 'Sarpras-Sas-3 of 5',
        'Sarpras-Sas-4 of 5', 'Sarpras-Sas-5 of 5', 'Sarpras-Rat',
        'Dig-Sas-1 of 5', 'Dig-Sas-2 of 5', 'Dig-Sas-3 of 5',
        'Dig-Sas-4 of 5', 'Dig-Sas-5 of 5', 'Dig Rat',
        'Rata-rata Nilai'
    ]
    
    styled_df = display_df.style
    for col in rating_columns:
        if col in display_df.columns:
            styled_df = styled_df.map(color_rating, subset=[col])
    
    st.dataframe(styled_df, use_container_width=True, height=500)
    st.caption(f"Menampilkan {len(display_df)} baris data")
    
    # Download buttons
    col_download1, col_download2 = st.columns(2)
    download_df = filtered_df[display_columns].copy()
    
    for col in download_df.select_dtypes(include=[np.number]).columns:
        if col in ['P.Isi', 'P.Hadir']:
            download_df[col] = download_df[col].apply(lambda x: int(x) if pd.notna(x) else '')
        else:
            download_df[col] = download_df[col].apply(lambda x: round(x, 2) if pd.notna(x) else '')
    
    with col_download1:
        csv = download_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"data_penilaian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_download2:
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            download_df.to_excel(writer, index=False, sheet_name='Data Penilaian')
        excel_data = output.getvalue()
        st.download_button(
            label="📥 Download Excel",
            data=excel_data,
            file_name=f"data_penilaian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )