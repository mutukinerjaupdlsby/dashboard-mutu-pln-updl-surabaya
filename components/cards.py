# CARD
import streamlit as st

# single card
def render_scorecard(value, label, color="#0078d4", trend=None, trend_value=None):
    trend_html = ""
    if trend:
        trend_class = "trend-up" if trend == "up" else "trend-down" if trend == "down" else "trend-neutral"
        trend_symbol = "↑" if trend == "up" else "↓" if trend == "down" else "→"
        trend_html = f'<div class="scorecard-trend {trend_class}">{trend_symbol} {trend_value:.1f}%</div>'
    
    st.markdown(f"""
    <div class='scorecard'>
        <div class='scorecard-value' style='color: {color};'>{value}</div>
        <div class='scorecard-label'>{label}</div>
        {trend_html}
    </div>
    """, unsafe_allow_html=True)

# multiple metrik card
def render_metric_cards(metrics):
    if not metrics:
        return
    
    cols = st.columns(len(metrics))
    for idx, metric in enumerate(metrics):
        with cols[idx]:
            render_scorecard(
                metric.get("value", "N/A"),
                metric.get("label", ""),
                metric.get("color", "#0078d4"),
                metric.get("trend"),
                metric.get("trend_value")
            )

# KPI sentimen
def render_kpi_cards(total_data, positive_pct, neutral_pct, negative_pct):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value'>{total_data}</div>
            <div class='scorecard-label'>Total Data</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value' style='color: #28a745;'>{positive_pct:.1f}%</div>
            <div class='scorecard-label'>Positif</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value' style='color: #ffc107;'>{neutral_pct:.1f}%</div>
            <div class='scorecard-label'>Netral</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='scorecard'>
            <div class='scorecard-value' style='color: #dc3545;'>{negative_pct:.1f}%</div>
            <div class='scorecard-label'>Negatif</div>
        </div>
        """, unsafe_allow_html=True)