import os
import sys
import textwrap
import streamlit as st
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import get_all_students
from src.data_processing import filter_dataframe
from src.statistics import calculate_correlation_matrix
from src.visualizations import (
    create_scatter_sm_vs_marks,
    create_scatter_study_vs_marks,
    create_scatter_sm_vs_study,
    create_bar_avg_marks_by_usage,
    create_hist_social_media,
    create_hist_academic_marks,
    create_boxplot_marks_by_usage,
    create_correlation_heatmap
)

st.html(textwrap.dedent("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 2rem; color: #111827; margin: 0 0 0.25rem 0;">📈 Interactive Data Visualizations</h1>
        <p style="color: #64748B; font-size: 1rem; margin: 0;">Explore interactive Plotly charts with dynamic filtering by course, gender, platform, and usage ranges.</p>
    </div>
"""))

raw_df = get_all_students()

if raw_df.empty:
    st.warning("⚠️ No student records available to visualize.")
    st.stop()

# ----------------- SIDEBAR INTERACTIVE FILTERS -----------------
with st.sidebar:
    st.markdown("### 🎛️ Interactive Filters")
    
    courses_avail = ["All"] + sorted(raw_df["course"].dropna().unique().tolist())
    sel_courses = st.multiselect("Select Course(s):", options=courses_avail, default=["All"])

    genders_avail = ["All"] + sorted(raw_df["gender"].dropna().unique().tolist())
    sel_genders = st.multiselect("Select Gender(s):", options=genders_avail, default=["All"])

    platforms_avail = ["All"] + sorted(raw_df["platform"].dropna().unique().tolist())
    sel_platforms = st.multiselect("Select Platform(s):", options=platforms_avail, default=["All"])

    max_sm_val = float(raw_df["social_media_hours"].max())
    
    sm_range = st.slider(
        "Social Media Hours Range:",
        min_value=0.0,
        max_value=24.0,
        value=(0.0, max_sm_val),
        step=0.5
    )

# Filter Dataframe
filtered_df = filter_dataframe(
    raw_df,
    selected_courses=sel_courses,
    selected_genders=sel_genders,
    selected_platforms=sel_platforms,
    sm_hours_range=sm_range
)

st.markdown(f"**Filtered Sample Size:** `n = {len(filtered_df)}` students of `{len(raw_df)}` total.")

if filtered_df.empty:
    st.warning("No records match the selected filter criteria. Please broaden your sidebar selection.")
    st.stop()

# ----------------- CHARTS TABS -----------------
tab_scatter, tab_dist, tab_box_bar, tab_heat = st.tabs([
    "📌 Scatter Plots & Trends",
    "📊 Distributions",
    "📦 Cohort Comparisons",
    "🔥 Correlation Heatmap"
])

# Tab 1: Scatter Plots
with tab_scatter:
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.plotly_chart(create_scatter_sm_vs_marks(filtered_df), use_container_width=True)
    with c2:
        with st.container(border=True):
            st.plotly_chart(create_scatter_study_vs_marks(filtered_df), use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(create_scatter_sm_vs_study(filtered_df), use_container_width=True)

# Tab 2: Histograms
with tab_dist:
    h1, h2 = st.columns(2)
    with h1:
        with st.container(border=True):
            st.plotly_chart(create_hist_social_media(filtered_df), use_container_width=True)
    with h2:
        with st.container(border=True):
            st.plotly_chart(create_hist_academic_marks(filtered_df), use_container_width=True)

# Tab 3: Box Plots & Bar Charts
with tab_box_bar:
    with st.container(border=True):
        col_thresh1, col_thresh2 = st.columns(2)
        with col_thresh1:
            low_t = st.number_input("Low Usage Threshold (< hrs):", value=2.0, min_value=0.5, max_value=12.0, step=0.5)
        with col_thresh2:
            mod_t = st.number_input("Moderate Usage Upper Limit (<= hrs):", value=4.0, min_value=1.0, max_value=18.0, step=0.5)

        bb1, bb2 = st.columns(2)
        with bb1:
            st.plotly_chart(create_bar_avg_marks_by_usage(filtered_df, low_t, mod_t), use_container_width=True)
        with bb2:
            st.plotly_chart(create_boxplot_marks_by_usage(filtered_df, low_t, mod_t), use_container_width=True)

# Tab 4: Heatmap
with tab_heat:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="saas-card-header">
                <div class="saas-card-title">Filtered Correlation Heatmap Matrix</div>
            </div>
        """))
        corr_matrix_filt = calculate_correlation_matrix(filtered_df)
        st.plotly_chart(create_correlation_heatmap(corr_matrix_filt), use_container_width=True)
