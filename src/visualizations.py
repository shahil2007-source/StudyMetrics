import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from src.data_processing import categorize_usage

# SaaS Design Tokens
COLOR_NAVY = "#111827"
COLOR_INDIGO = "#6366F1"
COLOR_BLUE = "#3B82F6"
COLOR_EMERALD = "#10B981"
COLOR_AMBER = "#F59E0B"
COLOR_ROSE = "#F43F5E"
COLOR_GRID = "rgba(226, 232, 240, 0.7)"
BG_TRANSPARENT = "rgba(0,0,0,0)"

FONT_FAMILY = "Plus Jakarta Sans, Inter, -apple-system, sans-serif"


def _apply_saas_chart_style(fig, title: str, x_title: str, y_title: str):
    """Applies sleek SaaS styling to Plotly figure with optimized dimensions."""
    fig.update_layout(
        height=480,
        title=dict(
            text=f"<b>{title}</b>",
            y=0.96,
            x=0.0,
            xanchor='left',
            font=dict(size=17, family=FONT_FAMILY, color=COLOR_NAVY)
        ),
        xaxis_title=dict(text=x_title, font=dict(size=13, family=FONT_FAMILY, color="#475569")),
        yaxis_title=dict(text=y_title, font=dict(size=13, family=FONT_FAMILY, color="#475569")),
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor="#FFFFFF",
        font=dict(family=FONT_FAMILY, size=12, color="#334155"),
        margin=dict(l=45, r=25, t=45, b=45),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=13,
            font_family=FONT_FAMILY,
            font_color="#FFFFFF"
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            font=dict(size=12, family=FONT_FAMILY)
        )
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_GRID, zeroline=False)
    return fig


def create_scatter_sm_vs_marks(df: pd.DataFrame) -> go.Figure:
    """Scatter plot: Social media usage vs. academic marks with OLS trendline."""
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="social_media_hours",
        y="academic_marks",
        color="platform",
        size="study_hours",
        hover_data=["student_id", "course", "attendance"],
        trendline="ols",
        trendline_color_override=COLOR_ROSE,
        color_discrete_sequence=[COLOR_INDIGO, COLOR_BLUE, COLOR_EMERALD, COLOR_AMBER, "#8B5CF6", "#EC4899", "#14B8A6"]
    )

    fig = _apply_saas_chart_style(
        fig,
        title="Social Media Usage vs. Academic Marks (%)",
        x_title="Daily Social Media Usage (Hours)",
        y_title="Academic Marks (%)"
    )
    return fig


def create_scatter_study_vs_marks(df: pd.DataFrame) -> go.Figure:
    """Scatter plot: Study hours vs. academic marks with OLS trendline."""
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="study_hours",
        y="academic_marks",
        color="course",
        hover_data=["student_id", "social_media_hours", "attendance"],
        trendline="ols",
        trendline_color_override=COLOR_EMERALD,
        color_discrete_sequence=[COLOR_INDIGO, COLOR_BLUE, COLOR_EMERALD, COLOR_AMBER, "#8B5CF6", "#EC4899", "#06B6D4", "#F97316"]
    )

    fig = _apply_saas_chart_style(
        fig,
        title="Study Hours vs. Academic Marks (%)",
        x_title="Daily Study Hours",
        y_title="Academic Marks (%)"
    )
    return fig


def create_scatter_sm_vs_study(df: pd.DataFrame) -> go.Figure:
    """Scatter plot: Social media usage vs. study hours with OLS trendline."""
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="social_media_hours",
        y="study_hours",
        color="gender",
        hover_data=["student_id", "academic_marks"],
        trendline="ols",
        trendline_color_override=COLOR_INDIGO,
        color_discrete_sequence=[COLOR_INDIGO, COLOR_EMERALD, COLOR_AMBER, "#64748B"]
    )

    fig = _apply_saas_chart_style(
        fig,
        title="Social Media Usage vs. Study Hours",
        x_title="Daily Social Media Usage (Hours)",
        y_title="Daily Study Hours"
    )
    return fig


def create_bar_avg_marks_by_usage(df: pd.DataFrame, low_t=2.0, mod_t=4.0) -> go.Figure:
    """Bar chart: Average academic marks by social media usage group."""
    if df.empty:
        return go.Figure()

    df_cat = categorize_usage(df, low_t, mod_t)
    grouped = df_cat.groupby("usage_group")["academic_marks"].agg(["mean", "std", "count"]).reset_index()

    group_order = [f"Low (<{low_t}h)", f"Moderate ({low_t}-{mod_t}h)", f"High (>{mod_t}h)"]
    grouped["order"] = grouped["usage_group"].apply(lambda x: group_order.index(x) if x in group_order else 99)
    grouped = grouped.sort_values("order")

    fig = px.bar(
        grouped,
        x="usage_group",
        y="mean",
        text=grouped["mean"].apply(lambda v: f"{v:.1f}%"),
        color="usage_group",
        color_discrete_map={
            group_order[0]: COLOR_EMERALD,
            group_order[1]: COLOR_INDIGO,
            group_order[2]: COLOR_ROSE
        }
    )

    fig.update_traces(
        textposition='outside',
        marker=dict(line=dict(color='rgba(0,0,0,0.1)', width=1), cornerradius=6)
    )

    fig = _apply_saas_chart_style(
        fig,
        title="Average Academic Marks by Social Media Tier",
        x_title="Social Media Tier",
        y_title="Mean Academic Marks (%)"
    )
    fig.update_layout(showlegend=False, yaxis_range=[0, 105])
    return fig


def create_hist_social_media(df: pd.DataFrame) -> go.Figure:
    """Histogram: Distribution of social media usage."""
    if df.empty:
        return go.Figure()

    mean_sm = df["social_media_hours"].mean()

    fig = px.histogram(
        df,
        x="social_media_hours",
        nbins=16,
        color_discrete_sequence=[COLOR_INDIGO],
        marginal="box"
    )

    fig.add_vline(
        x=mean_sm,
        line_dash="dash",
        line_color=COLOR_ROSE,
        annotation_text=f"Mean: {mean_sm:.1f}h",
        annotation_position="top right"
    )

    fig = _apply_saas_chart_style(
        fig,
        title="Distribution of Daily Social Media Usage",
        x_title="Social Media Usage (Hours/Day)",
        y_title="Student Count"
    )
    return fig


def create_hist_academic_marks(df: pd.DataFrame) -> go.Figure:
    """Histogram: Distribution of academic marks."""
    if df.empty:
        return go.Figure()

    mean_marks = df["academic_marks"].mean()

    fig = px.histogram(
        df,
        x="academic_marks",
        nbins=16,
        color_discrete_sequence=[COLOR_EMERALD],
        marginal="box"
    )

    fig.add_vline(
        x=mean_marks,
        line_dash="dash",
        line_color=COLOR_INDIGO,
        annotation_text=f"Mean: {mean_marks:.1f}%",
        annotation_position="top right"
    )

    fig = _apply_saas_chart_style(
        fig,
        title="Distribution of Academic Marks (%)",
        x_title="Academic Marks (%)",
        y_title="Student Count"
    )
    return fig


def create_boxplot_marks_by_usage(df: pd.DataFrame, low_t=2.0, mod_t=4.0) -> go.Figure:
    """Box plot: Academic marks across social media usage groups."""
    if df.empty:
        return go.Figure()

    df_cat = categorize_usage(df, low_t, mod_t)
    group_order = [f"Low (<{low_t}h)", f"Moderate ({low_t}-{mod_t}h)", f"High (>{mod_t}h)"]

    fig = px.box(
        df_cat,
        x="usage_group",
        y="academic_marks",
        color="usage_group",
        category_orders={"usage_group": group_order},
        points="all",
        hover_data=["student_id", "course"],
        color_discrete_map={
            group_order[0]: COLOR_EMERALD,
            group_order[1]: COLOR_INDIGO,
            group_order[2]: COLOR_ROSE
        }
    )

    fig = _apply_saas_chart_style(
        fig,
        title="Academic Marks Distribution across Usage Groups",
        x_title="Social Media Usage Group",
        y_title="Academic Marks (%)"
    )
    fig.update_layout(showlegend=False)
    return fig


def create_correlation_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """Correlation heatmap for numerical variables."""
    if corr_df.empty:
        return go.Figure()

    z_vals = corr_df.values
    x_labels = corr_df.columns.tolist()
    y_labels = corr_df.index.tolist()

    annotations = []
    for i, row in enumerate(z_vals):
        for j, val in enumerate(row):
            annotations.append(
                dict(
                    text=f"<b>{val:.2f}</b>",
                    x=x_labels[j],
                    y=y_labels[i],
                    xref="x1",
                    yref="y1",
                    showarrow=False,
                    font=dict(color="white" if abs(val) > 0.45 else COLOR_NAVY, size=13, family=FONT_FAMILY)
                )
            )

    fig = go.Figure(
        data=go.Heatmap(
            z=z_vals,
            x=x_labels,
            y=y_labels,
            colorscale=[
                [0.0, COLOR_ROSE],
                [0.5, "#F8FAFC"],
                [1.0, COLOR_EMERALD]
            ],
            zmin=-1.0,
            zmax=1.0,
            colorbar=dict(title="r", tickvals=[-1, -0.5, 0, 0.5, 1])
        )
    )

    fig.update_layout(annotations=annotations)
    fig = _apply_saas_chart_style(
        fig,
        title="Pearson Correlation Heatmap Matrix",
        x_title="",
        y_title=""
    )
    return fig
