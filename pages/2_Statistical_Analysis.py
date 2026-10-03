import os
import sys
import textwrap
import streamlit as st
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import get_all_students
from src.statistics import (
    calculate_pearson_correlation,
    calculate_spearman_correlation,
    calculate_descriptive_stats,
    calculate_correlation_matrix
)
from src.visualizations import create_correlation_heatmap

st.html(textwrap.dedent("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 2rem; color: #111827; margin: 0 0 0.25rem 0;">🧮 Statistical Analysis Engine</h1>
        <p style="color: #64748B; font-size: 1rem; margin: 0;">Parametric Pearson & Non-parametric Spearman correlation modeling, descriptive summaries, and heatmap matrix.</p>
    </div>
"""))

df = get_all_students()

if df.empty or len(df) < 3:
    st.error("⚠️ Insufficient data (minimum 3 records required) to compute reliable statistical tests.")
    st.stop()

# Helper for card rendering
def render_stat_card(title: str, corr_val: float, p_val: float, sample_n: int, strength: str, direction: str, is_sig: bool, interp: str):
    badge_bg = "#FEF2F2" if corr_val < 0 else ("#ECFDF5" if corr_val > 0 else "#F1F5F9")
    badge_color = "#EF4444" if corr_val < 0 else ("#10B981" if corr_val > 0 else "#64748B")
    sig_text = "Significant (p < 0.05)" if is_sig else "Not Significant"
    sig_color = "#10B981" if is_sig else "#F59E0B"
    
    html_card = textwrap.dedent(f"""
        <div class="saas-card-box">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <div style="font-weight: 700; font-size: 1.1rem; color: #111827;">{title}</div>
                <div style="background: {badge_bg}; color: {badge_color}; font-weight: 700; font-size: 0.85rem; padding: 0.25rem 0.65rem; border-radius: 9999px;">
                    {direction} ({strength})
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1rem; background: #F8FAFC; padding: 0.85rem; border-radius: 10px;">
                <div>
                    <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">COEFFICIENT</div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: {badge_color};">{corr_val:+.4f}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">P-VALUE</div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #1E293B;">{p_val:.5f}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">SIGNIFICANCE</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: {sig_color}; margin-top: 0.2rem;">{sig_text}</div>
                </div>
            </div>
            
            <div style="font-size: 0.875rem; color: #334155; line-height: 1.5;">
                <b>Interpretation:</b> {interp}
            </div>
        </div>
    """)
    st.html(html_card)


# ----------------- PEARSON CORRELATION -----------------
st.subheader("A. Pearson Bivariate Correlation (Linear Association)")
p_sm_marks = calculate_pearson_correlation(df["social_media_hours"], df["academic_marks"])
p_study_marks = calculate_pearson_correlation(df["study_hours"], df["academic_marks"])

col_p1, col_p2 = st.columns(2)

with col_p1:
    render_stat_card(
        "📱 Social Media Usage vs. Academic Marks",
        p_sm_marks['r'],
        p_sm_marks['p_value'],
        p_sm_marks['sample_size'],
        p_sm_marks['strength'],
        p_sm_marks['direction'],
        p_sm_marks['statistically_significant'],
        p_sm_marks['interpretation']
    )

with col_p2:
    render_stat_card(
        "📚 Study Hours vs. Academic Marks",
        p_study_marks['r'],
        p_study_marks['p_value'],
        p_study_marks['sample_size'],
        p_study_marks['strength'],
        p_study_marks['direction'],
        p_study_marks['statistically_significant'],
        p_study_marks['interpretation']
    )

st.markdown("---")

# ----------------- SPEARMAN CORRELATION -----------------
st.subheader("B. Spearman Rank-Order Correlation (Monotonic Association)")
s_sm_marks = calculate_spearman_correlation(df["social_media_hours"], df["academic_marks"])
s_study_marks = calculate_spearman_correlation(df["study_hours"], df["academic_marks"])

col_s1, col_s2 = st.columns(2)

with col_s1:
    render_stat_card(
        "📱 Social Media Usage vs. Academic Marks",
        s_sm_marks['rho'],
        s_sm_marks['p_value'],
        s_sm_marks['sample_size'],
        s_sm_marks['strength'],
        s_sm_marks['direction'],
        s_sm_marks['statistically_significant'],
        s_sm_marks['interpretation']
    )

with col_s2:
    render_stat_card(
        "📚 Study Hours vs. Academic Marks",
        s_study_marks['rho'],
        s_study_marks['p_value'],
        s_study_marks['sample_size'],
        s_study_marks['strength'],
        s_study_marks['direction'],
        s_study_marks['statistically_significant'],
        s_study_marks['interpretation']
    )

st.markdown("---")

# ----------------- DESCRIPTIVE STATISTICS -----------------
with st.container(border=True):
    st.html(textwrap.dedent("""
        <div class="saas-card-header">
            <div class="saas-card-title">C. Descriptive Statistics Summary</div>
        </div>
    """))
    desc_df = calculate_descriptive_stats(df)
    st.dataframe(desc_df, use_container_width=True, hide_index=True)

# ----------------- CORRELATION MATRIX & HEATMAP -----------------
with st.container(border=True):
    st.html(textwrap.dedent("""
        <div class="saas-card-header">
            <div class="saas-card-title">D. Correlation Matrix Heatmap</div>
        </div>
    """))
    matrix_cols = st.columns([2, 3])

    with matrix_cols[0]:
        corr_df = calculate_correlation_matrix(df)
        st.markdown("**Pairwise Matrix Table:**")
        st.dataframe(corr_df, use_container_width=True)

    with matrix_cols[1]:
        fig_heatmap = create_correlation_heatmap(corr_df)
        st.plotly_chart(fig_heatmap, use_container_width=True)
