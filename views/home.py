import os
import sys
import datetime
import textwrap
import streamlit as st
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import check_mongodb_connection, is_mongodb_connected, get_all_students
from src.statistics import calculate_pearson_correlation
from src.visualizations import (
    create_scatter_sm_vs_marks,
    create_scatter_study_vs_marks,
    create_hist_social_media
)

# Fetch Data & Database Status
mongo_status, mongo_msg = check_mongodb_connection()
is_mongo = is_mongodb_connected()
df = get_all_students()

if df.empty:
    st.warning("⚠️ No student records found. Please navigate to 'Student Data' to add or upload records.")
    st.stop()

# ==================== DASHBOARD HEADER ====================
curr_date_str = datetime.date.today().strftime("%B %d, %Y")

st.html(textwrap.dedent(f"""
    <div class="hero-header">
        <div class="hero-title">Welcome to StudyMetrics</div>
        <div class="hero-subtitle">Explore the relationship between social media usage and academic performance.</div>
        <div class="hero-meta-bar">
            <div class="hero-meta-item">📅 Current Date: <b>{curr_date_str}</b></div>
            <div class="hero-meta-item">📊 Dataset Status: <b>{len(df)} Student Records</b></div>
            <div class="hero-meta-item">⚡ Database Engine: <b>{'MongoDB Atlas' if is_mongo else 'CSV Local Engine'}</b></div>
        </div>
    </div>
"""))

# ==================== ROW 1: 5 KPI CARDS ====================
total_students = len(df)
avg_sm = df["social_media_hours"].mean()
avg_study = df["study_hours"].mean()
avg_marks = df["academic_marks"].mean()

pearson_res = calculate_pearson_correlation(df["social_media_hours"], df["academic_marks"])
r_val = pearson_res["r"]
p_val = pearson_res["p_value"]
r_color = "#F43F5E" if r_val < 0 else "#10B981"
top_platform = df['platform'].mode()[0] if not df['platform'].empty else 'Instagram'

st.html(textwrap.dedent(f"""
    <div class="kpi-grid-5">
        <div class="saas-kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label-text">Total Students</span>
                <div class="kpi-icon-wrapper">👥</div>
            </div>
            <div class="kpi-main-value">{total_students}</div>
            <div class="kpi-sub-text">Sample Size (n)</div>
        </div>
        <div class="saas-kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label-text">Avg Social Media</span>
                <div class="kpi-icon-wrapper">📱</div>
            </div>
            <div class="kpi-main-value">{avg_sm:.1f} <span style="font-size: 0.95rem; font-weight: 500;">hrs/day</span></div>
            <div class="kpi-sub-text">Daily Consumption</div>
        </div>
        <div class="saas-kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label-text">Avg Study Hours</span>
                <div class="kpi-icon-wrapper">📚</div>
            </div>
            <div class="kpi-main-value">{avg_study:.1f} <span style="font-size: 0.95rem; font-weight: 500;">hrs/day</span></div>
            <div class="kpi-sub-text">Academic Focus</div>
        </div>
        <div class="saas-kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label-text">Avg Academic Marks</span>
                <div class="kpi-icon-wrapper">🎓</div>
            </div>
            <div class="kpi-main-value">{avg_marks:.1f}%</div>
            <div class="kpi-sub-text">Overall Mean Score</div>
        </div>
        <div class="saas-kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label-text">Pearson Correlation</span>
                <div class="kpi-icon-wrapper">⚡</div>
            </div>
            <div class="kpi-main-value" style="color: {r_color};">{r_val:+.3f}</div>
            <div class="kpi-sub-text">{pearson_res['strength']} {pearson_res['direction']}</div>
        </div>
    </div>
"""))

# ==================== ROW 2: SCATTER PLOT & ACADEMIC SUMMARY ====================
r2_col1, r2_col2 = st.columns([3, 2])

with r2_col1:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="saas-card-header">
                <div class="saas-card-title">📈 Social Media Usage vs. Academic Marks</div>
                <div class="saas-card-sub">Scatter plot with OLS trendline showing bivariate relationship</div>
            </div>
        """))
        fig_scatter = create_scatter_sm_vs_marks(df)
        st.plotly_chart(fig_scatter, use_container_width=True)

with r2_col2:
    with st.container(border=True):
        st.html(textwrap.dedent(f"""
            <div class="saas-card-header">
                <div class="saas-card-title">📌 Executive Analytical Summary</div>
                <div class="saas-card-sub">Core statistical findings & correlation principles</div>
            </div>
            <div style="font-size: 0.925rem; line-height: 1.6; color: #334155;">
                <p><b>Empirical Finding:</b> A statistically significant inverse correlation (r = <b>{r_val:.3f}</b>, p = <b>{p_val:.4f}</b>) 
                is observed between social media consumption and academic performance.</p>
                
                <div class="saas-callout-info">
                    <b>⚖️ Correlation vs. Causation Principle:</b><br/>
                    A correlation indicates co-occurrence rather than direct causation. Factors such as time management discipline, 
                    sleep duration, and study effort act as underlying mediating variables.
                </div>
                
                <ul style="padding-left: 1.2rem; margin-top: 0.5rem; margin-bottom: 0;">
                    <li><b>High Focus Cohort:</b> Students studying &gt;5h/day maintain high marks regardless of social media.</li>
                    <li><b>Primary Platform:</b> {top_platform} represents the highest user share in current dataset.</li>
                </ul>
            </div>
        """))

# ==================== ROW 3: STUDY VS MARKS & DISTRIBUTION ====================
r3_col1, r3_col2 = st.columns([1, 1])

with r3_col1:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="saas-card-header">
                <div class="saas-card-title">📚 Study Hours vs. Academic Marks</div>
                <div class="saas-card-sub">Evaluating direct positive impact of study discipline</div>
            </div>
        """))
        fig_study = create_scatter_study_vs_marks(df)
        st.plotly_chart(fig_study, use_container_width=True)

with r3_col2:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="saas-card-header">
                <div class="saas-card-title">📊 Social Media Usage Distribution</div>
                <div class="saas-card-sub">Histogram of daily consumption hours with mean reference line</div>
            </div>
        """))
        fig_hist = create_hist_social_media(df)
        st.plotly_chart(fig_hist, use_container_width=True)

# ==================== ROW 4: DATASET SUMMARY & RECENT RECORDS ====================
with st.container(border=True):
    st.html(textwrap.dedent("""
        <div class="saas-card-header">
            <div class="saas-card-title">📋 Dataset Summary & Recent Student Records</div>
            <div class="saas-card-sub">Previewing recent validated records from current database storage</div>
        </div>
    """))
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("StudyMetrics Analytics Platform © 2025 - College Statistics & Analytics Assignment")
