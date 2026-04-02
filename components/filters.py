# FILTER
import streamlit as st
import pandas as pd
from datetime import datetime

def render_date_filter(df, date_column, key_prefix=""):
    if date_column not in df.columns:
        return None, None
    if df[date_column].isna().all():
        return None, None
    
    min_date = df[date_column].min()
    max_date = df[date_column].max()
    
    if pd.isna(min_date) or pd.isna(max_date):
        return None, None
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Tanggal Mulai",value=min_date, min_value=min_date, max_value=max_date, key=f"{key_prefix}_start_date")
    with col2:
        end_date = st.date_input("Tanggal Akhir",value=max_date, min_value=min_date,max_value=max_date, key=f"{key_prefix}_end_date")
    
    return start_date, end_date

# select filter
def render_select_filter(df, column, label, key_prefix=""):
    if column not in df.columns:
        return "Semua"
    values = df[column].dropna().unique().tolist()
    options = ["Semua"] + sorted([str(x) for x in values if str(x) != ''])

    selected = st.selectbox(label, options, key=f"{key_prefix}_{column}")
    return selected

# multiselect filter
def render_multiselect_filter(df, column, label, key_prefix=""):
    if column not in df.columns:
        return []
    values = df[column].dropna().unique().tolist()
    options = sorted([str(x) for x in values if str(x) != ''])
    
    selected = st.multiselect(label, options, default=[], key=f"{key_prefix}_{column}")
    return selected

# search bar (text input)
def render_search_filter(label="🔍 Cari", placeholder="Masukkan kata kunci...", key_prefix=""):
    search_term = st.text_input(
        label,
        placeholder=placeholder,
        key=f"{key_prefix}_search"
    )
    return search_term

# apply multiple filter
def apply_filters(df, filters):
    filtered_df = df.copy()
    for col, value in filters.items():
        if value is None or value == "":
            continue
        
        if col == "search" and value:
            # Apply search to all text columns
            text_columns = filtered_df.select_dtypes(include=['object']).columns
            mask = pd.Series([False] * len(filtered_df))
            for text_col in text_columns:
                mask = mask | filtered_df[text_col].astype(str).str.contains(value, case=False, na=False)
            filtered_df = filtered_df[mask]
        
        elif isinstance(value, list) and value:
            # Multiselect filter
            filtered_df = filtered_df[filtered_df[col].isin(value)]
        
        elif value != "Semua" and value != "All" and value != "":
            # Single select filter
            filtered_df = filtered_df[filtered_df[col] == value]
    
    return filtered_df

# render a complete filter section with multiple filters
def render_filter_section(df, filters_config):
    filters = {}
    with st.container():
        st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
        st.markdown("<p class='filter-title'>🔍 Filter Data</p>", unsafe_allow_html=True)
        
        # Kolom filter berdasarkan jumlah filter
        num_filters = len(filters_config)
        cols = st.columns(min(num_filters, 4))
        
        for idx, config in enumerate(filters_config):
            col_idx = idx % 4
            with cols[col_idx]:
                if config["type"] == "select":
                    value = render_select_filter(
                        df,
                        config["column"],
                        config["label"],
                        config.get("key_prefix", "")
                    )
                    filters[config["column"]] = value
                
                elif config["type"] == "multiselect":
                    value = render_multiselect_filter(
                        df,
                        config["column"],
                        config["label"],
                        config.get("key_prefix", "")
                    )
                    filters[config["column"]] = value
                
                elif config["type"] == "search":
                    value = render_search_filter(
                        config.get("label", "🔍 Cari"),
                        config.get("placeholder", "Masukkan kata kunci..."),
                        config.get("key_prefix", "")
                    )
                    filters["search"] = value
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    return apply_filters(df, filters)