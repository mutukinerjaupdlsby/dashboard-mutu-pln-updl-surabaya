import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import format_time

def render_sistem_nlp():
    st.title("Sistem NLP - Test Version")
    st.write("Jika ini muncul, berarti file berhasil di-load")
    
    tab1, tab2 = st.tabs(["Import File", "Input Teks"])
    
    with tab1:
        st.write("Tab Import File - Coming Soon")
    
    with tab2:
        st.write("Tab Input Teks - Coming Soon")

if __name__ == "__main__":
    render_sistem_nlp()