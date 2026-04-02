# utils/styling.py
import streamlit as st

def load_css():
    """Load custom CSS styling"""
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .st-emotion-cache-1y4p8pa {
            display: none !important;
        }

        section[data-testid="stSidebar"] ul {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] a {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .stMarkdown:has(a) {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 300px !important;
            width: 300px !important;
            background: linear-gradient(180deg, var(--background-color) 0%, rgba(0,0,0,0.02) 100%);
            border-right: 1px solid rgba(128, 128, 128, 0.2);
            padding-top: 20px !important;
            flex-shrink: 0 !important;
            position: relative !important;
            transform: none !important;
            left: 0 !important;
        }

        section[data-testid="stSidebar"] .stButton {
            display: block !important;
            visibility: visible !important;
        }
        
        section[data-testid="stSidebar"] .stImage {
            display: flex !important;
            visibility: visible !important;
        }
        
        section[data-testid="stSidebar"] hr {
            display: block !important;
        }

        .main .block-container {
            max-width: calc(100% - 300px) !important;
            margin-left: auto !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        /* Sidebar logo styling */
        [data-testid="stSidebar"] .stImage {
            display: flex !important;
            justify-content: center !important;
            margin: -60px auto 5px auto !important;
        }
        
        [data-testid="stSidebar"] .stImage img {
            width: 100px !important;
            height: auto !important;
            margin: 0 auto !important;
            display: block !important;
        }
        
        .sidebar-title {
            text-align: center;
            font-size: 1rem !important;
            font-weight: 600;
            margin: 15px 0 25px 0 !important;
            padding: 0 10px !important;
            letter-spacing: 0.5px;
            color: var(--text-color);
            background: linear-gradient(135deg, #0078d4, #00a8e8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        [data-testid="stSidebar"] .stButton > button {
            width: 90% !important;
            height: 50px !important;
            margin: 5px auto !important;
            border-radius: 12px !important;
            border: none !important;
            background-color: transparent !important;
            color: var(--text-color) !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            padding-left: 25px !important;
            transition: all 0.3s ease !important;
            border: 1px solid rgba(128, 128, 128, 0.1) !important;
            display: block !important;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: rgba(0, 120, 212, 0.1) !important;
            border: 1px solid rgba(0, 120, 212, 0.3) !important;
            transform: translateX(1px);
        }
        
        [data-testid="stSidebar"] .stButton > button:active {
            background-color: rgba(0, 120, 212, 0.2) !important;
        }
        
        [data-testid="stSidebar"] .stButton > button:focus {
            background-color: rgba(0, 120, 212, 0.15) !important;
            border-left: 4px solid #0078d4 !important;
        }
        
        /* Main action button styling */
        .stButton > button {
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        [data-theme="light"] .stButton > button {
            background: linear-gradient(135deg, #e6f3ff, #d4eaff) !important;
            color: #0078d4 !important;
            border: 1px solid #b8d9ff !important;
        }
        
        [data-theme="light"] .stButton > button:hover {
            background: linear-gradient(135deg, #d4eaff, #c0e0ff) !important;
            border-color: #0078d4 !important;
            box-shadow: 0 4px 12px rgba(0,120,212,0.2) !important;
        }
        
        [data-theme="dark"] .stButton > button {
            background: linear-gradient(135deg, #2d2d2d, #3d3d3d) !important;
            color: #e0e0e0 !important;
            border: 1px solid #4a4a4a !important;
        }
        
        [data-theme="dark"] .stButton > button:hover {
            background: linear-gradient(135deg, #3d3d3d, #4d4d4d) !important;
            border-color: #0078d4 !important;
            box-shadow: 0 4px 12px rgba(0,120,212,0.3) !important;
            color: #ffffff !important;
        }

        .stDownloadButton > button {
            font-weight: 600 !important;
        }
        
        [data-theme="light"] .stDownloadButton > button {
            background: linear-gradient(135deg, #e6f3ff, #d4eaff) !important;
            color: #0078d4 !important;
            border: 1px solid #b8d9ff !important;
        }
        
        [data-theme="dark"] .stDownloadButton > button {
            background: linear-gradient(135deg, #2d2d2d, #3d3d3d) !important;
            color: #e0e0e0 !important;
            border: 1px solid #4a4a4a !important;
        }
        
        [data-theme="dark"] .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #3d3d3d, #4d4d4d) !important;
            border-color: #0078d4 !important;
            color: #ffffff !important;
        }
        
        /* Header styling */
        .page-header {
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(0, 120, 212, 0.1);
        }
        
        .page-title {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #0078d4, #00a8e8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 0.5rem 0 !important;
        }
        
        .page-description {
            font-size: 1rem !important;
            opacity: 0.8;
            color: var(--text-color);
            margin-left: 0.5rem !important;
        }
        
        /* Card styling */
        .card {
            background: var(--background-color);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 20px;
            padding: 1.8rem;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.03);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            backdrop-filter: blur(10px);
            margin-bottom: 20px;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0, 120, 212, 0.1);
            border-color: rgba(0, 120, 212, 0.2);
        }
        
        /* Scorecard styling */
        .scorecard {
            background: linear-gradient(135deg, rgba(0, 120, 212, 0.05), rgba(0, 168, 232, 0.05));
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(0, 120, 212, 0.2);
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .scorecard:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0, 120, 212, 0.15);
            border-color: rgba(0, 120, 212, 0.4);
        }
        
        .scorecard-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0078d4;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }
        
        .scorecard-label {
            font-size: 0.55rem;
            opacity: 0.9;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }
        
        /* Metric styling */
        .metric-container {
            display: flex;
            justify-content: space-around;
            margin: 20px 0 30px 0;
            padding: 25px;
            background: linear-gradient(135deg, rgba(0, 120, 212, 0.05), rgba(0, 168, 232, 0.05));
            border-radius: 20px;
            border: 1px solid rgba(128, 128, 128, 0.1);
        }
        
        .metric-item {
            text-align: center;
            flex: 1;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #0078d4;
            line-height: 1.2;
        }
        
        .metric-label {
            font-size: 0.95rem;
            opacity: 0.8;
            font-weight: 500;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent !important;
            padding: 0 !important;
            border-radius: 0 !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px 12px 0 0 !important;
            padding: 10px 25px !important;
            font-weight: 600 !important;
            background-color: transparent !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            color: var(--text-color) !important;
            text-transform: none !important;
        }
        
        .stTabs [aria-selected="true"] {
            color: #0078d4 !important;
            border-bottom: 2px solid #0078d4 !important;
            background-color: transparent !important;
        }
        
        .info-badge {
            display: inline-block;
            padding: 8px 16px;
            background: linear-gradient(135deg, rgba(0,120,212,0.1), rgba(0,168,232,0.1));
            border-radius: 30px;
            font-size: 0.9rem;
            margin-bottom: 20px;
            border: 0.5px solid rgba(0,120,212,0.2);
            color: var(--text-color) !important;
            backdrop-filter: blur(5px);
        }
        
        [data-theme="dark"] .info-badge {
            background: linear-gradient(135deg, rgba(0,120,212,0.2), rgba(0,168,232,0.2));
            border-color: rgba(0,120,212,0.3);
            color: #ffffff !important;
        }
        
        [data-theme="light"] .info-badge {
            background: linear-gradient(135deg, rgba(0,120,212,0.05), rgba(0,168,232,0.05));
            border-color: rgba(0,120,212,0.2);
            color: #000000 !important;
        }
        
        @media (max-width: 768px) {
            section[data-testid="stSidebar"] {
                min-width: 100% !important;
                max-width: 100% !important;
                width: 100% !important;
            }
            
            .main .block-container {
                max-width: 100% !important;
                margin-left: 0 !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            
            .metric-container {
                flex-direction: column;
                gap: 20px;
            }
        }
    </style>
    """, unsafe_allow_html=True)