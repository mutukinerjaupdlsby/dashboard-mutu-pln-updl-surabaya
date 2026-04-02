# CHART
import altair as alt
import plotly.express as px
import streamlit as st
import pandas as pd

# sentimen bar chart
def render_sentiment_bar_chart(data, title="Distribusi Sentimen"):
    if data.empty or "Sentimen" not in data.columns:
        st.info("Tidak ada data untuk ditampilkan")
        return
    sentiment_counts = data["Sentimen"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentimen", "Jumlah"]
    total = sentiment_counts["Jumlah"].sum()
    
    if total == 0:
        st.info("Tidak ada data untuk ditampilkan")
        return
    
    chart = alt.Chart(sentiment_counts).mark_bar(cornerRadius=5, size=90).encode(
        x=alt.X('Sentimen:N',
                axis=alt.Axis(labelAngle=0, title=None),
                sort=['Positif', 'Netral', 'Negatif']),
        y=alt.Y('Jumlah:Q', title='Jumlah'),
        color=alt.Color('Sentimen:N', scale=alt.Scale(
            domain=['Positif', 'Netral', 'Negatif'],
            range=['#28a745', '#ffc107', '#dc3545']
        )),
        tooltip=['Sentimen', 'Jumlah']
    )
    text = chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        fontSize=12,
        fontWeight=600,
        color='var(--text-color)'
    ).encode(text='Jumlah:Q')
    
    st.altair_chart(chart + text, use_container_width=True)

# sentimen pie chart
def render_sentiment_pie_chart(data, title="Persentase Sentimen"):
    if data.empty or "Sentimen" not in data.columns:
        st.info("Tidak ada data untuk ditampilkan")
        return
    sentiment_counts = data["Sentimen"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentimen", "Jumlah"]
    total = sentiment_counts["Jumlah"].sum()
    
    if total == 0:
        st.info("Tidak ada data untuk ditampilkan")
        return
    
    sentiment_counts["Persen"] = (sentiment_counts["Jumlah"] / total * 100)
    
    chart = alt.Chart(sentiment_counts).mark_arc(cornerRadius=4, outerRadius=125).encode(
        theta=alt.Theta(field='Jumlah', type='quantitative'),
        color=alt.Color('Sentimen:N', scale=alt.Scale(
            domain=['Positif', 'Netral', 'Negatif'],
            range=['#28a745', '#ffc107', '#dc3545']
        )),
        tooltip=[
            alt.Tooltip('Sentimen:N', title='Sentimen'),
            alt.Tooltip('Jumlah:Q', title='Jumlah'),
            alt.Tooltip('Persen:Q', format='.1f', title='Persentase %')
        ]
    )
    text = chart.mark_text(
        radius=140,
        size=12,
        fontWeight=600,
        color='var(--text-color)'
    ).encode(text=alt.Text('Persen:Q', format='.1f'))
    
    st.altair_chart(chart + text, use_container_width=True)

# trend line
def render_trend_line_chart(data, x_col, y_col, title="Tren Data", y_range=None):
    if data.empty:
        st.info("Tidak ada data untuk ditampilkan")
        return None
    
    fig = px.line(
        data,
        x=x_col,
        y=y_col,
        markers=True,
        text=data[y_col].apply(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else ""),
        title=title
    )
    fig.update_traces(
        textposition='top center',
        line=dict(color='#0078d4', width=3),
        marker=dict(size=10, color='#0078d4', line=dict(color='white', width=1))
    )
    
    layout_config = {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'xaxis': dict(gridcolor='rgba(128,128,128,0.1)', title_font=dict(size=12)),
        'yaxis': dict(gridcolor='rgba(128,128,128,0.1)', title_font=dict(size=12)),
        'height': 400,
        'hovermode': 'x unified'
    }
    
    if y_range:
        layout_config['yaxis']['range'] = y_range
    
    fig.update_layout(**layout_config)
    return fig

# bar chart distribution
def render_distribution_bar_chart(data, column, title="Distribusi Data", color="#00a8e8"):
    if data.empty or column not in data.columns:
        st.info("Tidak ada data untuk ditampilkan")
        return
    
    counts = data[column].value_counts().reset_index()
    counts.columns = [column, 'Frekuensi']
    counts = counts.sort_values('Frekuensi', ascending=False)
    
    fig = px.bar(
        counts,
        x=column,
        y='Frekuensi',
        title=title,
        text='Frekuensi',
        color_discrete_sequence=[color]
    )
    fig.update_traces(
        textposition='outside',
        textfont=dict(size=12, color=color),
        marker=dict(line=dict(color='rgba(0,0,0,0.2)', width=1))
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
        yaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# heatmap
def render_heatmap(data, x_col, y_col, values_col, title="Heatmap", colorscale='Blues'):
    if data.empty:
        st.info("Tidak ada data untuk ditampilkan")
        return
    
    pivot_data = pd.pivot_table(
        data,
        values=values_col,
        index=y_col,
        columns=x_col,
        aggfunc='count',
        fill_value=0
    )
    
    fig = px.imshow(
        pivot_data,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=colorscale,
        title=title,
        labels=dict(x=x_col, y=y_col, color="Jumlah")
    )
    fig.update_layout(
        height=500,
        xaxis=dict(tickangle=-45),
        yaxis=dict(autorange="reversed")
    )
    fig.update_traces(
        textfont=dict(size=12),
        hovertemplate=f'{y_col}: %{{y}}<br>{x_col}: %{{x}}<br>Jumlah: %{{z}}<extra></extra>'
    )
    st.plotly_chart(fig, use_container_width=True)

# wordcloud
def render_wordcloud_chart(text, title="Word Cloud", colormap='Blues'):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    
    if not text or len(text.strip()) == 0:
        st.info("Tidak cukup data untuk word cloud")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    
    wc = WordCloud(
        width=800,
        height=500,
        background_color=None,
        mode='RGBA',
        colormap=colormap,
        max_words=100,
        contour_width=1,
        random_state=42,
        collocations=False
    ).generate(text)
    
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.title(title, pad=20, fontsize=14, fontweight='bold')
    plt.tight_layout(pad=0)
    
    st.pyplot(fig, use_container_width=True)

# top word bar chart
def render_top_words_chart(words_df, title="Top 10 Kata", color="#0078d4"):
    if words_df.empty:
        st.info("Tidak ada data untuk ditampilkan")
        return
    
    chart = alt.Chart(words_df.head(10)).mark_bar(cornerRadius=4, color=color).encode(
        x=alt.X("Frekuensi:Q", title="Frekuensi"),
        y=alt.Y("Kata:N", sort="-x", title=None),
        tooltip=["Kata", "Frekuensi"]
    ).properties(height=350, title=title)
    
    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=5,
        fontSize=11,
        fontWeight=600,
        color=color
    ).encode(text='Frekuensi:Q')
    
    st.altair_chart(chart + text, use_container_width=True)
    