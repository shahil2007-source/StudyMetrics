import os
import sys

# Ensure project root directory is in sys.path for Streamlit Cloud compatibility
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from src.database import check_mongodb_connection, is_mongodb_connected

# Page Config
st.set_page_config(
    page_title="StudyMetrics - Student Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = os.path.join(PROJECT_ROOT, "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Database Connection Check
mongo_status, mongo_msg = check_mongodb_connection()
is_mongo = is_mongodb_connected()

# Sidebar Header Branding & High-Contrast Navigation
with st.sidebar:
    st.markdown("""<div class="sidebar-brand-box">
        <div class="brand-title-row">
            <div class="brand-logo-svg">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
            </div>
            <div>
                <div class="brand-name">StudyMetrics</div>
                <div class="brand-subtitle">Student Analytics Platform</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 🔌 Database Status")
        if is_mongo:
            st.markdown('<div class="status-pill-mongo">🟢 MongoDB Atlas Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-pill-csv">🔵 Local CSV Storage Fallback</div>', unsafe_allow_html=True)
        st.caption(f"Status: {mongo_msg}")

# Define Navigation Pages (5 Core Pages)
dashboard_page = st.Page("views/home.py", title="Dashboard", icon="📊", default=True)
data_page = st.Page("pages/1_Student_Data.py", title="Student Data", icon="📋")
stat_page = st.Page("pages/2_Statistical_Analysis.py", title="Statistical Analysis", icon="🧮")
vis_page = st.Page("pages/3_Data_Visualization.py", title="Data Visualization", icon="📈")
perf_page = st.Page("pages/4_Performance_Analysis.py", title="Performance Analysis", icon="🎓")

# Run Navigation
pg = st.navigation(
    {"Navigation": [dashboard_page, data_page, stat_page, vis_page, perf_page]},
    position="sidebar"
)
pg.run()
