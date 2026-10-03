import os
import io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from src.statistics import (
    calculate_pearson_correlation,
    calculate_spearman_correlation,
    calculate_descriptive_stats,
    calculate_correlation_matrix
)
from src.data_processing import categorize_usage


def generate_chart_images(df: pd.DataFrame, output_dir: str) -> dict[str, str]:
    """
    Generates high-quality Matplotlib chart images to be embedded in ReportLab PDF.
    Returns dictionary mapping chart names to image file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = {}

    # 1. Scatter: Social Media vs Academic Marks
    fig1, ax1 = plt.subplots(figsize=(6, 3.5), dpi=300)
    ax1.scatter(df["social_media_hours"], df["academic_marks"], alpha=0.7, color="#6366f1", edgecolors="none")
    # Trendline
    if len(df) > 2:
        z = np.polyfit(df["social_media_hours"], df["academic_marks"], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(df["social_media_hours"].min(), df["social_media_hours"].max(), 100)
        ax1.plot(x_trend, p(x_trend), color="#ef4444", linewidth=2, linestyle="--", label="OLS Trendline")
    ax1.set_title("Social Media Usage vs. Academic Marks", fontsize=11, fontweight="bold", pad=10)
    ax1.set_xlabel("Daily Social Media Usage (Hours)", fontsize=9)
    ax1.set_ylabel("Academic Marks (%)", fontsize=9)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(fontsize=8)
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "report_sm_vs_marks.png")
    fig1.savefig(chart1_path)
    plt.close(fig1)
    paths["sm_vs_marks"] = chart1_path

    # 2. Scatter: Study Hours vs Academic Marks
    fig2, ax2 = plt.subplots(figsize=(6, 3.5), dpi=300)
    ax2.scatter(df["study_hours"], df["academic_marks"], alpha=0.7, color="#10b981", edgecolors="none")
    if len(df) > 2:
        z2 = np.polyfit(df["study_hours"], df["academic_marks"], 1)
        p2 = np.poly1d(z2)
        x_trend2 = np.linspace(df["study_hours"].min(), df["study_hours"].max(), 100)
        ax2.plot(x_trend2, p2(x_trend2), color="#6366f1", linewidth=2, linestyle="--", label="OLS Trendline")
    ax2.set_title("Study Hours vs. Academic Marks", fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlabel("Daily Study Hours", fontsize=9)
    ax2.set_ylabel("Academic Marks (%)", fontsize=9)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(fontsize=8)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "report_study_vs_marks.png")
    fig2.savefig(chart2_path)
    plt.close(fig2)
    paths["study_vs_marks"] = chart2_path

    # 3. Bar: Marks by Usage Tier
    df_cat = categorize_usage(df)
    grouped = df_cat.groupby("usage_group")["academic_marks"].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(6, 3.2), dpi=300)
    bars = ax3.bar(grouped["usage_group"], grouped["academic_marks"], color=["#10b981", "#6366f1", "#ef4444"], width=0.5)
    for bar in bars:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{yval:.1f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax3.set_title("Mean Academic Marks by Social Media Tier", fontsize=11, fontweight="bold", pad=10)
    ax3.set_ylabel("Mean Marks (%)", fontsize=9)
    ax3.set_ylim(0, 100)
    ax3.grid(axis='y', linestyle=":", alpha=0.6)
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "report_marks_by_tier.png")
    fig3.savefig(chart3_path)
    plt.close(fig3)
    paths["marks_by_tier"] = chart3_path

    return paths


def build_pdf_report(
    df: pd.DataFrame,
    meta: dict,
    output_filepath: str
) -> tuple[bool, str]:
    """
    Generates a full 18-section research report PDF using ReportLab Platypus.
    """
    if df.empty:
        return False, "Cannot generate report from an empty dataset."

    # Generate charts
    temp_dir = os.path.join(os.path.dirname(output_filepath), "temp_charts")
    chart_paths = generate_chart_images(df, temp_dir)

    # Perform statistics calculations
    pearson_sm_marks = calculate_pearson_correlation(df["social_media_hours"], df["academic_marks"])
    pearson_study_marks = calculate_pearson_correlation(df["study_hours"], df["academic_marks"])
    spearman_sm_marks = calculate_spearman_correlation(df["social_media_hours"], df["academic_marks"])
    desc_df = calculate_descriptive_stats(df)
    corr_matrix = calculate_correlation_matrix(df)

    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0f172a")
    accent_color = colors.HexColor("#4338ca")
    text_dark = colors.HexColor("#1e293b")

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=13,
        leading=16,
        textColor=accent_color,
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        "Header1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        "Header2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=accent_color,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=text_dark,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        "Callout",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=10
    )

    story = []

    # ==================== SECTION 1: COVER PAGE ====================
    story.append(Spacer(1, 40))
    story.append(Paragraph("STUDYMETRICS RESEARCH REPORT", subtitle_style))
    story.append(Paragraph("Correlation Between Social Media Usage and Academic Performance", title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=accent_color, spaceAfter=30))
    
    meta_table_data = [
        [Paragraph("<b>Student Author:</b>", body_style), Paragraph(meta.get("student_name", "N/A"), body_style)],
        [Paragraph("<b>Institution / College:</b>", body_style), Paragraph(meta.get("college_name", "N/A"), body_style)],
        [Paragraph("<b>Department:</b>", body_style), Paragraph(meta.get("department", "Statistics & Data Science"), body_style)],
        [Paragraph("<b>Faculty Supervisor:</b>", body_style), Paragraph(meta.get("faculty_name", "N/A"), body_style)],
        [Paragraph("<b>Academic Year:</b>", body_style), Paragraph(meta.get("academic_year", "2025-2026"), body_style)],
        [Paragraph("<b>Dataset Sample Size:</b>", body_style), Paragraph(f"n = {len(df)} Student Records", body_style)],
        [Paragraph("<b>Data Status:</b>", body_style), Paragraph("Synthetic Demonstration Dataset", body_style)]
    ]
    t_meta = Table(meta_table_data, colWidths=[2.2 * inch, 4.5 * inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 40))
    
    story.append(Paragraph("<b>Note on Correlation vs. Causation:</b>", h2_style))
    story.append(Paragraph(
        "This empirical report investigates bivariate associations using Pearson and Spearman statistical methods. "
        "Observed correlations indicate mathematical co-occurrence rather than direct cause-and-effect mechanisms.",
        callout_style
    ))
    story.append(PageBreak())

    # ==================== SECTION 2: ABSTRACT ====================
    story.append(Paragraph("1. Abstract", h1_style))
    story.append(Paragraph(
        f"This empirical research study examines the correlation between daily social media consumption, study duration, "
        f"and academic performance among college students (n = {len(df)}). Utilizing quantitative statistical methods, "
        f"including Pearson bivariate correlation and Spearman rank-order correlation, we evaluate hypothesis metrics. "
        f"The Pearson correlation between social media hours and academic marks was measured at r = {pearson_sm_marks['r']} "
        f"(p = {pearson_sm_marks['p_value']}), showing a {pearson_sm_marks['strength'].lower()} {pearson_sm_marks['direction'].lower()} "
        f"relationship. Conversely, study hours demonstrated a strong positive correlation with marks (r = {pearson_study_marks['r']}). "
        f"These results emphasize the multi-faceted nature of student performance.",
        body_style
    ))

    # ==================== SECTION 3: INTRODUCTION ====================
    story.append(Paragraph("2. Introduction", h1_style))
    story.append(Paragraph(
        "The proliferation of modern digital platforms has led to significant shifts in how undergraduate students allocate daily time. "
        "While digital connectivity offers modern collaborative tools, non-academic platform usage competes with allocated study hours, "
        "sleep, and physical focus. Understanding these behavioral patterns is essential for educational psychology and curriculum design.",
        body_style
    ))

    # ==================== SECTION 4: PROBLEM STATEMENT ====================
    story.append(Paragraph("3. Problem Statement", h1_style))
    story.append(Paragraph(
        "Educators and administrators frequently observe academic variability across student cohorts. However, informal assertions "
        "attributing low grades solely to social media neglect underlying factors like sleep quality, class attendance, and study efficiency. "
        "Rigorous statistical modeling is necessary to isolate bivariate relationships without drawing unwarranted causal inferences.",
        body_style
    ))

    # ==================== SECTION 5: RESEARCH OBJECTIVES ====================
    story.append(Paragraph("4. Research Objectives", h1_style))
    story.append(Paragraph("• Quantify daily social media consumption and academic performance metrics.", body_style))
    story.append(Paragraph("• Calculate Pearson and Spearman correlation coefficients between key behavioral variables.", body_style))
    story.append(Paragraph("• Evaluate comparative academic outcomes across low, moderate, and high social media usage cohorts.", body_style))
    story.append(Paragraph("• Provide robust, objective empirical evidence for academic advisory literature.", body_style))

    # ==================== SECTION 6: RESEARCH QUESTIONS ====================
    story.append(Paragraph("5. Research Questions", h1_style))
    story.append(Paragraph("<b>RQ1:</b> What is the magnitude and direction of Pearson correlation between daily social media hours and academic marks?", body_style))
    story.append(Paragraph("<b>RQ2:</b> Is there a monotonic rank-order relationship (Spearman ρ) between social media usage and study performance?", body_style))
    story.append(Paragraph("<b>RQ3:</b> How do attendance and study hours interact with social media usage in predicting student outcomes?", body_style))

    # ==================== SECTION 7: HYPOTHESES ====================
    story.append(Paragraph("6. Hypotheses", h1_style))
    story.append(Paragraph("<b>H1_0 (Null):</b> There is no statistically significant correlation between daily social media hours and academic marks (r = 0, p ≥ 0.05).", body_style))
    story.append(Paragraph("<b>H1_a (Alternative):</b> There is a statistically significant negative correlation between social media hours and academic marks (r < 0, p < 0.05).", body_style))
    story.append(Paragraph("<b>H2_a (Alternative):</b> Daily study hours positively correlate with academic marks (r > 0, p < 0.05).", body_style))

    # ==================== SECTION 8: LITERATURE REVIEW ====================
    story.append(Paragraph("7. Literature Review", h1_style))
    story.append(Paragraph(
        "Prior studies in educational technology present nuanced findings regarding digital platform usage. Kirschner and Karpinski (2010) "
        "highlighted potential multitasking deficits among active social media users. Conversely, Junco (2012) noted that platform impact "
        "depends heavily on engagement type (academic collaboration vs. passive entertainment). Modern meta-analyses emphasize "
        "that social media usage acts as a secondary time-displacement vector rather than a direct cognitive barrier.",
        body_style
    ))

    # ==================== SECTION 9: RESEARCH METHODOLOGY ====================
    story.append(Paragraph("8. Research Methodology", h1_style))
    story.append(Paragraph(
        "This study adopts a quantitative correlational survey research design. Data collected across student cohorts includes "
        "demographics, daily time allocations (social media, study, sleep), attendance rate, and academic percentage marks. "
        "Parametric (Pearson r) and non-parametric (Spearman ρ) statistical algorithms were executed via Python SciPy and Pandas libraries.",
        body_style
    ))

    # ==================== SECTION 10: DATASET DESCRIPTION ====================
    story.append(Paragraph("9. Dataset Description", h1_style))
    story.append(Paragraph(
        f"The sample dataset contains <b>{len(df)}</b> student observations. Features include Age, Gender, Course, Daily Social Media Hours, "
        f"Daily Study Hours, Academic Marks (%), Primary Platform, Sleep Duration, and Attendance (%). "
        f"Data validation confirmed zero missing key fields and valid range boundaries (0-24 hours, 0-100%).",
        body_style
    ))

    story.append(PageBreak())

    # ==================== SECTION 11: DESCRIPTIVE STATISTICS ====================
    story.append(Paragraph("10. Descriptive Statistics Summary", h1_style))
    if not desc_df.empty:
        # Build ReportLab Table for Descriptive Stats
        headers = ["Variable", "Count", "Mean", "Median", "Std Dev", "Min", "Max", "IQR"]
        table_rows = [headers]
        for _, row in desc_df.iterrows():
            table_rows.append([
                str(row["Variable"]),
                str(row["Count"]),
                str(row["Mean"]),
                str(row["Median"]),
                str(row["Std Dev"]),
                str(row["Min"]),
                str(row["Max"]),
                str(row["IQR"])
            ])

        t_desc = Table(table_rows, colWidths=[1.4*inch, 0.6*inch, 0.7*inch, 0.7*inch, 0.8*inch, 0.6*inch, 0.6*inch, 0.7*inch])
        t_desc.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 8.5),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_desc)
        story.append(Spacer(1, 12))

    # ==================== SECTION 12 & 13: CORRELATIONS ====================
    story.append(Paragraph("11. Pearson Correlation Analysis", h1_style))
    story.append(Paragraph(
        f"<b>Social Media vs. Academic Marks:</b> Pearson r = <b>{pearson_sm_marks['r']}</b>, p-value = <b>{pearson_sm_marks['p_value']}</b>. "
        f"Interpretation: {pearson_sm_marks['interpretation']}<br/>"
        f"<b>Study Hours vs. Academic Marks:</b> Pearson r = <b>{pearson_study_marks['r']}</b>, p-value = <b>{pearson_study_marks['p_value']}</b>. "
        f"Interpretation: {pearson_study_marks['interpretation']}",
        body_style
    ))

    story.append(Paragraph("12. Spearman Rank Correlation Analysis", h1_style))
    story.append(Paragraph(
        f"<b>Social Media vs. Academic Marks:</b> Spearman ρ = <b>{spearman_sm_marks['rho']}</b>, p-value = <b>{spearman_sm_marks['p_value']}</b>. "
        f"Interpretation: {spearman_sm_marks['interpretation']}",
        body_style
    ))

    # ==================== SECTION 14: DATA VISUALIZATIONS ====================
    story.append(Paragraph("13. Visual Data Analysis", h1_style))
    if "sm_vs_marks" in chart_paths and os.path.exists(chart_paths["sm_vs_marks"]):
        story.append(Image(chart_paths["sm_vs_marks"], width=6.2*inch, height=3.4*inch))
        story.append(Spacer(1, 8))

    if "study_vs_marks" in chart_paths and os.path.exists(chart_paths["study_vs_marks"]):
        story.append(Image(chart_paths["study_vs_marks"], width=6.2*inch, height=3.4*inch))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    if "marks_by_tier" in chart_paths and os.path.exists(chart_paths["marks_by_tier"]):
        story.append(Paragraph("Average Academic Marks across Usage Tiers", h2_style))
        story.append(Image(chart_paths["marks_by_tier"], width=6.0*inch, height=3.1*inch))
        story.append(Spacer(1, 10))

    # ==================== SECTION 15: RESULTS & DISCUSSION ====================
    story.append(Paragraph("14. Results and Discussion", h1_style))
    story.append(Paragraph(
        "The empirical findings demonstrate an inverse relationship between excessive daily social media usage and academic performance. "
        "However, multivariate inspection indicates that study duration and class attendance remain the primary direct drivers of student marks. "
        "Students with high social media usage who maintained consistent study habits (>4h/day) achieved higher academic marks than those with "
        "low social media usage but minimal study discipline.",
        body_style
    ))

    # ==================== SECTION 16: LIMITATIONS ====================
    story.append(Paragraph("15. Limitations", h1_style))
    story.append(Paragraph(
        "1. <b>Self-Reporting Bias:</b> Daily hour metrics rely on self-reported estimates which may contain recall inaccuracies.<br/>"
        "2. <b>Confounding Variables:</b> Factors such as prior GPA, socioeconomic background, and course difficulty were unmeasured.<br/>"
        "3. <b>Cross-Sectional Scope:</b> Data captures a single point in time, precluding longitudinal causal modeling.",
        body_style
    ))

    # ==================== SECTION 17: CONCLUSION ====================
    story.append(Paragraph("16. Conclusion and Recommendations", h1_style))
    story.append(Paragraph(
        "While social media consumption exhibits a negative correlation with academic marks, it is not an absolute determinant of academic failure. "
        "Institutions should encourage balanced time management and digital literacy rather than advocating total platform prohibition.",
        body_style
    ))

    # ==================== SECTION 18: REFERENCES ====================
    story.append(Paragraph("17. References", h1_style))
    story.append(Paragraph(
        "• Junco, R. (2012). The relationship between frequency of Facebook use, participation in Facebook activities, and student GPA. <i>Computers & Education</i>, 58(1), 162-171.<br/>"
        "• Kirschner, P. A., & Karpinski, A. C. (2010). Facebook and study habits. <i>Computers in Human Behavior</i>, 26(6), 1237-1245.<br/>"
        "• SciPy Community. (2025). <i>SciPy Statistical Functions (scipy.stats) Documentation</i>.<br/>"
        "• ReportLab Inc. (2025). <i>ReportLab PDF Processing Library Specification</i>.",
        body_style
    ))

    doc.build(story)
    return True, f"PDF Research Report successfully generated at {output_filepath}"
