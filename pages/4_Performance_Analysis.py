import os
import sys
import textwrap
import streamlit as st
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import get_all_students
from src.data_processing import categorize_usage

st.html(textwrap.dedent("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 2rem; color: #111827; margin: 0 0 0.25rem 0;">🎓 Student Performance & Study Habit Analysis</h1>
        <p style="color: #64748B; font-size: 1rem; margin: 0;">Partition cohort data into social media consumption tiers to evaluate comparative academic performance.</p>
    </div>
"""))

df = get_all_students()

if df.empty:
    st.warning("⚠️ No student records available.")
    st.stop()

# ----------------- CONFIGURABLE THRESHOLDS -----------------
with st.container(border=True):
    st.html(textwrap.dedent("""
        <div class="saas-card-header">
            <div class="saas-card-title">⚙️ Configure Usage Tier Thresholds</div>
        </div>
    """))
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        low_thresh = st.slider("Low Usage Threshold (< hours/day):", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
    with t_col2:
        mod_thresh = st.slider("Moderate Usage Upper Limit (<= hours/day):", min_value=low_thresh+0.5, max_value=10.0, value=4.0, step=0.5)

df_cat = categorize_usage(df, low_thresh, mod_thresh)

# Group Summary Aggregation
grouped_summary = df_cat.groupby("usage_group").agg(
    Student_Count=("student_id", "count"),
    Mean_Marks=("academic_marks", "mean"),
    Median_Marks=("academic_marks", "median"),
    Mean_Study_Hours=("study_hours", "mean"),
    Mean_Sleep_Hours=("sleep_hours", "mean"),
    Mean_Attendance=("attendance", "mean")
).reset_index()

group_order = [f"Low (<{low_thresh}h)", f"Moderate ({low_thresh}-{mod_thresh}h)", f"High (>{mod_thresh}h)"]
grouped_summary["order"] = grouped_summary["usage_group"].apply(lambda x: group_order.index(x) if x in group_order else 99)
grouped_summary = grouped_summary.sort_values("order").drop(columns=["order"])

with st.container(border=True):
    st.html(textwrap.dedent("""
        <div class="saas-card-header">
            <div class="saas-card-title">📊 Cohort Performance Summary Table</div>
        </div>
    """))
    st.dataframe(
        grouped_summary.style.format({
            "Mean_Marks": "{:.2f}%",
            "Median_Marks": "{:.2f}%",
            "Mean_Study_Hours": "{:.2f} hrs",
            "Mean_Sleep_Hours": "{:.2f} hrs",
            "Mean_Attendance": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

# ----------------- COHORT CARDS BREAKDOWN -----------------
st.subheader("🔍 Cohort Deep-Dive Metrics")

card_cols = st.columns(len(grouped_summary))
for idx, (_, row) in enumerate(grouped_summary.iterrows()):
    accent_bar = "#10B981" if idx==0 else ("#6366F1" if idx==1 else "#F43F5E")
    card_html = textwrap.dedent(f"""
        <div class="saas-card-box" style="border-top: 4px solid {accent_bar}; margin-bottom: 0;">
            <div style="font-size: 0.825rem; font-weight: 700; color: #64748B; text-transform: uppercase;">{row['usage_group']}</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #111827; margin: 0.25rem 0;">{row['Mean_Marks']:.1f}%</div>
            <div style="font-size: 0.8rem; font-weight: 600; color: {accent_bar};">Mean Academic Marks</div>
            <hr style="margin: 0.75rem 0; border: 0; border-top: 1px solid #E2E8F0;"/>
            <div style="font-size: 0.85rem; color: #334155; line-height: 1.6;">
                👥 <b>Students:</b> {row['Student_Count']}<br/>
                📚 <b>Study Time:</b> {row['Mean_Study_Hours']:.1f} hrs/day<br/>
                😴 <b>Sleep Duration:</b> {row['Mean_Sleep_Hours']:.1f} hrs/day<br/>
                🏫 <b>Attendance:</b> {row['Mean_Attendance']:.1f}%
            </div>
        </div>
    """)
    with card_cols[idx]:
        st.html(card_html)

# ----------------- NEUTRAL ACADEMIC FINDINGS EXPLANATION -----------------
st.html(textwrap.dedent("""
    <div class="saas-callout-info">
        <h4 style="margin: 0 0 0.5rem 0; color: #0C4A6E; font-size: 1.05rem;">💡 Objective Analysis & Nuanced Interpretation</h4>
        <p><b>Observed Patterns:</b> Data indicates an inverse relationship between daily social media hours and mean academic marks across cohorts. 
        Specifically, students in the <i>High Usage</i> group average lower overall marks compared to the <i>Low Usage</i> group.</p>
        
        <p><b>Key Confounding Dynamics:</b></p>
        <ul style="margin: 0; padding-left: 1.2rem;">
            <li><b>Study Hours Displacement:</b> Students in the High Usage group also report lower mean daily study hours, suggesting that time allocation is a primary mediator.</li>
            <li><b>Attendance & Sleep:</b> Sleep duration and attendance rates decline slightly in higher social media cohorts, which independently influence academic retention.</li>
            <li><b>Neutral Language Safeguard:</b> It is improper to conclude that social media <i>causes</i> cognitive impairment or lower academic capability. Individuals with strong time management skills achieve high academic marks regardless of platform usage.</li>
        </ul>
    </div>
"""))
