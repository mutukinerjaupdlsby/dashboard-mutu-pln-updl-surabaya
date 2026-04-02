# SIDEBAR 
import streamlit as st
from utils.config import PAGES

def render_sidebar():
    with st.sidebar:
        # Logo
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image(
                    "https://upload.wikimedia.org/wikipedia/commons/9/97/Logo_PLN.png",
                    use_container_width=True
                )
            except:
                st.markdown("<div style='text-align:center; font-size:2rem;'>⚡</div>", unsafe_allow_html=True)
        
        st.markdown("<p class='sidebar-title'>⚡ DASHBOARD LEARNING INSIGHT</p>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:0px 15px 35px 15px; border:0; border-top:0.5px solid #cccccc;'>", unsafe_allow_html=True)
        
        # Navigation button
        if st.button("EVALUASI L1", key="btn_evaluasi_l1", use_container_width=True):
            st.session_state.page = PAGES["Evaluasi L1"]
            st.rerun()
        if st.button("PENILAIAN", key="btn_penilaian", use_container_width=True):
            st.session_state.page = PAGES["Penilaian"]
            st.rerun()
        if st.button("SISTEM NLP", key="btn_sistem_nlp", use_container_width=True):
            st.session_state.page = PAGES["Sistem NLP"]
            st.rerun()
        if st.button("INFORMASI", key="btn_info", use_container_width=True):
            st.session_state.page = PAGES["Info"]
            st.rerun()
        
        st.markdown("<hr style='margin:15px 15px; border:0; border-top:0.5px solid #cccccc;'>", unsafe_allow_html=True)
        
        # Footer
        st.markdown(
            """
            <div style='text-align: center; opacity: 0.7; font-size: 0.8rem; padding: 10px;'>
                <p style='margin: 2px;'><b>Evaluasi & Pengendalian Mutu dan Kinerja</b></p>
                <p style='margin: 2px;'><b>PT PLN (Persero) UPDL Surabaya</b></p>
                <p style='margin: 10px 0 2px 0;'>© 2026</p>
            </div>
            """, unsafe_allow_html=True
        )