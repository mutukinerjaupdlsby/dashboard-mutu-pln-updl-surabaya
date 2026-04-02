# INFO
import streamlit as st

# Render Halaman Info
def render_info():
    st.markdown("""
    <div class='page-header'>
        <h3 class='page-subtitle'>ℹ️ Informasi Sistem</h3>
        <p class='page-description'>Detail informasi mengenai Dashboard Learning Insight</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h4 style='margin-top: 0; color: #0078d4; margin-bottom: 15px;'>📶 Dashboard Learning Insight</h4>
        <p style='font-size: 0.9rem; line-height: 1.6;'>
            Sistem ini dikembangkan untuk mempermudah proses tracking dan evaluasi ulasan peserta pembelajaran di <b>PT PLN (Persero) UPDL Surabaya</b>. 
            Melalui integrasi dengan <b>Google Sheets</b>, sistem mampu melakukan otomasi pengolahan data yang terhubung langsung dengan dashboard <b>Streamlit</b>. 
            Selain itu, sistem ini juga dilengkapi fitur <b>AI</b> untuk mengklasifikasikan sentimen, indikator, dan keluhan yang memungkinkan pengguna menambahkan file data dan 
            menganalisis data teks secara otomatis untuk memperoleh hasilnya dengan lebih cepat dan akurat.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h4 style='margin-top: 0; color: #0078d4; margin-bottom: 15px;'>🗃️ Data Management</h4>
        <p style='font-size: 0.9rem; line-height: 1.6;'>
            Data dikelola langsung oleh <b>Tim Evaluasi & Pengendalian Mutu dan Kinerja</b> secara terpusat melalui <b>Google Sheets</b> yang terintegrasi langsung dengan sistem Dashboard Learning Insight.
            Data dapat diakses di:
            <a href="https://docs.google.com/spreadsheets/d/1DtCoRzSXuXAM8MYBtiiSphNTzGplmgsPJEQfVWgRSe4/edit?usp=sharing" target="_blank" style="color:#0078d4; font-weight:500;">
                Lihat Data
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h4 style='color:#0078d4; margin-top:0; margin-bottom:18px;'>⚙️ Teknologi Sistem</h4>
        <div style='display:flex; flex-direction:column; gap:12px;'>
            <div style='background:rgba(0,120,212,0.05); padding:14px; border-radius:10px;'>
                <b>🧠 Sistem NLP</b><br>
                <small>
                Sistem NLP dibuat menggunakan algoritma <b>RoBERTa (Robustly Optimized BERT Approach)</b>, yaitu model Deep Learning berbasis Transformers.
                Model yang dibuat memiliki akurasi rata-rata <b>97-99%</b> baik untuk klasifikasi Sentimen, Indikator, dan Keluhan.
                </small>
            </div>
            <div style='background:rgba(0,120,212,0.05); padding:14px; border-radius:10px;'>
                <b>🗂️ Kategori Sentimen, Indikator, dan Keluhan</b><br>
                <small>
                Sistem NLP mengklasifikasikan ulasan ke dalam <b>3</b> kategori sentimen <b>(Positif, Netral, Negatif)</b>, dengan tambahan kategori <b>Invalid</b> untuk kasus 
                tertentu sesuai kebutuhan. Selain itu, terdapat model klasifikasi untuk <b>16 kategori Indikator</b> serta <b>32 kategori Keluhan</b> yang merupakan sub-kategori dari indikator tersebut.
                </small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h4 style='color: #0078d4; margin-top: 0; margin-bottom: 15px;'>👥 Tim</h4>
        <p><b>Departemen Evaluasi & Pengendalian Mutu dan Kinerja</b><br>PT PLN (Persero) UPDL Surabaya</p>
        <p><b>📧</b> evaluasi@pln.updl.ac.id</p>
    </div>
    """, unsafe_allow_html=True)