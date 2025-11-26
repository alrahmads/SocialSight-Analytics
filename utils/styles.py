import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown(
        """
<style>
    .blue-header {
        background-color: #1E50A0;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
 
    .blue-header h1 {
        color: white !important;
    }

    [data-testid="stSidebar"] {
        background-color: #1E50A0 !important;
    }

    [data-testid="stSidebar"] > :not(div[data-testid="stFileUploader"]) {
        color: white !important;
    }

    .stButton > button {
        background-color: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        width: 100% !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin-bottom: 6px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #4A90E2 !important;
        color: white !important;
        transform: translateX(5px);
    }

    .stButton > button[kind="primary"] {
        background-color: #4A90E2 !important;
        border: 2px solid white !important;
        color: white !important;
        font-weight: 700 !important;
    }

    div[data-testid="stFileUploader"] > label {
        color: white !important;
        font-weight: 700 !important;
    }

    div[data-testid="stFileUploader"] div[role="button"] {
        background-color: rgba(255,255,255,0.95) !important;
        border: 1px solid rgba(0,0,0,0.25) !important;
    }

    div[data-testid="stFileUploader"] small {
        color: black !important;
    }

    .st-emotion-cache-9ycgxx,
    .st-emotion-cache-9ycgxx *,
    .e1b2p2ww12,
    .e1b2p2ww12 * {
        color: black !important;
        -webkit-text-fill-color: black !important;
        opacity: 1 !important;
    }

    div[data-testid="stFileUploader"] button {
        background-color: #1E50A0 !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }

    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1E50A0;
    }
    
    div[data-testid="stMetric"] label {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #666 !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #1E50A0 !important;
    }
            
    .post-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
            
    .post-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.2);
    }
            
    .post-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
        color: white;
    }
    
    .post-channel {
        display: flex;
        align-items: center;
        font-size: 14px;
        margin-bottom: 15px;
        opacity: 0.9;
    }
            
    .post-stats {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .stat-item {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 14px;
        font-weight: 600;
    }
            
    .rank-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(255,255,255,0.3);
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.3rem; 
    }

    [data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-top: -50px; 
    }
</style>
""",
        unsafe_allow_html=True,
    )


def render_header():
    """Render page header"""
    st.markdown(
        """
<div class="blue-header">
    <h1 style="margin-bottom:5px;">SocialSight Analytics</h1>
    <p style="opacity: 0.8; margin-top:-5px;">Visual Analytics • Performance • Trend • Insight</p>
</div>
""",
        unsafe_allow_html=True,
    )