import os
import sys
import io
import tempfile
import pandas as pd
import numpy as np
from typing import Optional, List
from fastapi import FastAPI, HTTPException, UploadFile, File, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import (
    check_mongodb_connection,
    is_mongodb_connected,
    get_all_students,
    add_student_record,
    update_student_record,
    delete_student_record,
    save_all_students
)
from src.data_processing import (
    validate_student_data,
    process_uploaded_csv,
    filter_dataframe,
    categorize_usage
)
from src.statistics import (
    calculate_pearson_correlation,
    calculate_spearman_correlation,
    calculate_descriptive_stats,
    calculate_correlation_matrix
)
from src.report_generator import build_pdf_report

app = FastAPI(
    title="StudyMetrics API",
    description="FastAPI Serverless Backend for StudyMetrics Student Analytics",
    version="2.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentRecord(BaseModel):
    student_id: Optional[str] = Field(default=None)
    Student_ID: Optional[str] = Field(default=None)
    Name: Optional[str] = Field(default=None)
    age: int = Field(default=20, ge=15, le=100)
    gender: str = Field(default="Prefer not to say")
    course: str = Field(default="Computer Science")
    social_media_hours: Optional[float] = Field(default=None)
    Social_Media_Usage_Hours: Optional[float] = Field(default=None)
    study_hours: Optional[float] = Field(default=None)
    Study_Hours: Optional[float] = Field(default=None)
    academic_marks: Optional[float] = Field(default=None)
    Academic_Marks: Optional[float] = Field(default=None)
    platform: str = Field(default="Instagram")
    sleep_hours: float = Field(default=7.5, ge=0.0, le=24.0)
    attendance: float = Field(default=85.0, ge=0.0, le=100.0)

    def normalize(self) -> dict:
        sid = self.student_id or self.Student_ID or f"STU{np.random.randint(1000, 9999)}"
        sm = self.social_media_hours if self.social_media_hours is not None else (self.Social_Media_Usage_Hours or 3.0)
        st = self.study_hours if self.study_hours is not None else (self.Study_Hours or 5.0)
        marks = self.academic_marks if self.academic_marks is not None else (self.Academic_Marks or 75.0)
        return {
            "student_id": sid,
            "Student_ID": sid,
            "Name": self.Name or f"Student {sid}",
            "age": self.age,
            "gender": self.gender,
            "course": self.course,
            "social_media_hours": float(sm),
            "Social_Media_Usage_Hours": float(sm),
            "study_hours": float(st),
            "Study_Hours": float(st),
            "academic_marks": float(marks),
            "Academic_Marks": float(marks),
            "platform": self.platform,
            "sleep_hours": self.sleep_hours,
            "attendance": self.attendance
        }


class ReportMetadata(BaseModel):
    title: Optional[str] = Field(default="StudyMetrics Analytical Research Report")
    author: Optional[str] = Field(default="Department of Student Analytics")
    institution: Optional[str] = Field(default="StudyMetrics Educational Research Institute")
    targetAudience: Optional[str] = Field(default="Academic Deans & Student Success Officers")
    executiveSummary: Optional[str] = Field(default="Research report summary...")
    student_name: Optional[str] = Field(default="Shahilkumar Tankala")
    college_name: Optional[str] = Field(default="Department of Data Science & Statistics")
    department: Optional[str] = Field(default="School of Mathematical & Computational Sciences")
    faculty_name: Optional[str] = Field(default="Dr. A. R. Sharma")
    academic_year: Optional[str] = Field(default="2025 - 2026")


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "StudyMetrics FastAPI Backend"}


@app.get("/api/database/status")
def database_status():
    mongo_ok, msg = check_mongodb_connection()
    return {
        "connected": is_mongodb_connected(),
        "message": msg,
        "mode": "MongoDB Atlas" if is_mongodb_connected() else "CSV Fallback Storage"
    }


@app.get("/api/students")
def get_students(
    search: Optional[str] = None,
    course: Optional[str] = None,
    gender: Optional[str] = None,
    platform: Optional[str] = None,
    min_sm: Optional[float] = None,
    max_sm: Optional[float] = None
):
    df = get_all_students()
    if df.empty:
        return []

    # Apply search query
    if search:
        s = search.strip().lower()
        df = df[
            df["student_id"].astype(str).str.lower().str.contains(s) |
            df["course"].astype(str).str.lower().str.contains(s) |
            df["platform"].astype(str).str.lower().str.contains(s)
        ]

    # Apply filters
    courses_list = [course] if course and course != "All" else None
    genders_list = [gender] if gender and gender != "All" else None
    platforms_list = [platform] if platform and platform != "All" else None
    sm_range = (min_sm if min_sm is not None else 0.0, max_sm if max_sm is not None else 24.0)

    filtered_df = filter_dataframe(
        df,
        selected_courses=courses_list,
        selected_genders=genders_list,
        selected_platforms=platforms_list,
        sm_hours_range=sm_range
    )

    records = []
    for _, r in filtered_df.iterrows():
        sid = str(r.get("student_id", r.get("Student_ID", "")))
        sm = float(r.get("social_media_hours", r.get("Social_Media_Usage_Hours", 0.0)))
        st = float(r.get("study_hours", r.get("Study_Hours", 0.0)))
        marks = float(r.get("academic_marks", r.get("Academic_Marks", 0.0)))
        name = str(r.get("Name", r.get("name", f"Student {sid}")))
        records.append({
            "student_id": sid,
            "Student_ID": sid,
            "Name": name,
            "social_media_hours": sm,
            "Social_Media_Usage_Hours": sm,
            "study_hours": st,
            "Study_Hours": st,
            "academic_marks": marks,
            "Academic_Marks": marks,
            "course": r.get("course", "Computer Science"),
            "platform": r.get("platform", "Instagram"),
            "gender": r.get("gender", "Prefer not to say"),
            "age": r.get("age", 20)
        })

    return records


@app.post("/api/students")
def create_student(record: StudentRecord):
    data_dict = record.normalize()
    valid, msg = validate_student_data(data_dict)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    success, db_msg = add_student_record(data_dict)
    if not success:
        raise HTTPException(status_code=400, detail=db_msg)

    return {"status": "success", "message": db_msg, "record": data_dict}


@app.put("/api/students/{student_id}")
def edit_student(student_id: str, record: StudentRecord):
    data_dict = record.normalize()
    valid, msg = validate_student_data(data_dict)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    success, db_msg = update_student_record(student_id, data_dict)
    if not success:
        raise HTTPException(status_code=404, detail=db_msg)

    return {"status": "success", "message": db_msg}


@app.delete("/api/students/{student_id}")
def remove_student(student_id: str):
    success, db_msg = delete_student_record(student_id)
    if not success:
        raise HTTPException(status_code=404, detail=db_msg)

    return {"status": "success", "message": db_msg}


@app.post("/api/students/upload")
def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = file.file.read()
    buffer = io.BytesIO(content)
    cleaned_df, msgs = process_uploaded_csv(buffer)

    if cleaned_df.empty:
        raise HTTPException(status_code=400, detail="Uploaded CSV contains no valid records. " + " ".join(msgs))

    save_all_students(cleaned_df)
    return {
        "status": "success",
        "message": f"Successfully uploaded and saved {len(cleaned_df)} student records.",
        "warnings": msgs
    }


@app.get("/api/students/export")
def export_csv():
    df = get_all_students()
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = Response(content=stream.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=studymetrics_dataset.csv"
    return response


@app.get("/api/analytics/dashboard")
def get_dashboard_data():
    df = get_all_students()
    if df.empty:
        return {
            "summary": {
                "total_students": 0,
                "avg_social_media": 0.0,
                "avg_study_hours": 0.0,
                "avg_academic_marks": 0.0,
                "pearson_r": 0.0,
                "pearson_p": 0.0,
                "pearson_interpretation": "No data available",
                "spearman_rho": 0.0
            },
            "charts": {
                "social_vs_marks": {"x": [], "y": [], "hover_text": [], "trendline_x": [], "trendline_y": []},
                "study_vs_marks": {"x": [], "y": [], "hover_text": [], "trendline_x": [], "trendline_y": []}
            },
            "kpis": {
                "total_students": 0,
                "avg_social_media": 0.0,
                "avg_study_hours": 0.0,
                "avg_academic_marks": 0.0,
                "pearson_r": 0.0
            },
            "pearson": {}
        }

    total_students = len(df)
    avg_sm = round(float(df["social_media_hours"].mean()), 2)
    avg_study = round(float(df["study_hours"].mean()), 2)
    avg_marks = round(float(df["academic_marks"].mean()), 2)

    pearson_res = calculate_pearson_correlation(df["social_media_hours"], df["academic_marks"])
    spearman_res = calculate_spearman_correlation(df["social_media_hours"], df["academic_marks"])
    top_platform = str(df["platform"].mode()[0]) if not df["platform"].empty else "Instagram"

    # Social media vs marks scatter & regression line
    sm_x = df["social_media_hours"].tolist()
    sm_y = df["academic_marks"].tolist()
    names = df["student_id"].tolist()

    if len(df) >= 2:
        m_sm, b_sm = np.polyfit(sm_x, sm_y, 1)
        x_trend_sm = [float(min(sm_x)), float(max(sm_x))]
        y_trend_sm = [round(float(m_sm * x + b_sm), 2) for x in x_trend_sm]
    else:
        x_trend_sm, y_trend_sm = [], []

    # Study hours vs marks scatter & trendline
    st_x = df["study_hours"].tolist()
    st_y = df["academic_marks"].tolist()
    if len(df) >= 2:
        m_st, b_st = np.polyfit(st_x, st_y, 1)
        x_trend_st = [float(min(st_x)), float(max(st_x))]
        y_trend_st = [round(float(m_st * x + b_st), 2) for x in x_trend_st]
    else:
        x_trend_st, y_trend_st = [], []

    summary_data = {
        "total_students": total_students,
        "avg_social_media": avg_sm,
        "avg_study_hours": avg_study,
        "avg_academic_marks": avg_marks,
        "pearson_r": pearson_res["r"],
        "pearson_p": pearson_res["p_value"],
        "pearson_interpretation": pearson_res["interpretation"],
        "spearman_rho": spearman_res["rho"]
    }

    charts_data = {
        "social_vs_marks": {
            "x": sm_x,
            "y": sm_y,
            "hover_text": names,
            "trendline_x": x_trend_sm,
            "trendline_y": y_trend_sm
        },
        "study_vs_marks": {
            "x": st_x,
            "y": st_y,
            "hover_text": names,
            "trendline_x": x_trend_st,
            "trendline_y": y_trend_st
        }
    }

    return {
        "summary": summary_data,
        "charts": charts_data,
        "kpis": {
            "total_students": total_students,
            "avg_social_media": avg_sm,
            "avg_study_hours": avg_study,
            "avg_academic_marks": avg_marks,
            "pearson_r": pearson_res["r"]
        },
        "pearson": pearson_res,
        "top_platform": top_platform,
        "recent_records": df.head(10).to_dict(orient="records")
    }



@app.get("/api/analytics/statistics")
def get_statistics():
    df = get_all_students()
    if df.empty or len(df) < 3:
        raise HTTPException(status_code=400, detail="Insufficient data to compute statistical modeling.")

    pearson_sm = calculate_pearson_correlation(df["social_media_hours"], df["academic_marks"])
    pearson_study = calculate_pearson_correlation(df["study_hours"], df["academic_marks"])

    spearman_sm = calculate_spearman_correlation(df["social_media_hours"], df["academic_marks"])
    spearman_study = calculate_spearman_correlation(df["study_hours"], df["academic_marks"])

    desc_df = calculate_descriptive_stats(df)
    corr_df = calculate_correlation_matrix(df)

    # Reformat descriptive stats into clean list of dicts
    descriptive_list = []
    if not desc_df.empty:
        for _, row in desc_df.iterrows():
            descriptive_list.append({
                "Metric": row.get("Variable", ""),
                "Mean": row.get("Mean", 0.0),
                "Std": row.get("Std Dev", 0.0),
                "Min": row.get("Min", 0.0),
                "25%": row.get("Q1 (25%)", 0.0),
                "50%": row.get("Q2 (50%)", 0.0),
                "75%": row.get("Q3 (75%)", 0.0),
                "Max": row.get("Max", 0.0)
            })

    # Reformat correlation matrix for Plotly heatmap
    matrix_labels = ["Social Media", "Study Hours", "Academic Marks"]
    subset_cols = ["social_media_hours", "study_hours", "academic_marks"]
    if all(c in df.columns for c in subset_cols):
        sub_corr = df[subset_cols].corr().values.tolist()
        matrix_data = {
            "z": sub_corr,
            "x": matrix_labels,
            "y": matrix_labels
        }
    else:
        matrix_data = {
            "z": corr_df.values.tolist() if not corr_df.empty else [],
            "x": corr_df.columns.tolist() if not corr_df.empty else [],
            "y": corr_df.index.tolist() if not corr_df.empty else []
        }

    return {
        "pearson": pearson_sm,
        "spearman": spearman_sm,
        "pearson_details": {
            "sm_vs_marks": pearson_sm,
            "study_vs_marks": pearson_study
        },
        "spearman_details": {
            "sm_vs_marks": spearman_sm,
            "study_vs_marks": spearman_study
        },
        "descriptive": descriptive_list,
        "descriptive_stats": desc_df.to_dict(orient="records") if not desc_df.empty else [],
        "matrix": matrix_data,
        "correlation_matrix": {
            "columns": corr_df.columns.tolist() if not corr_df.empty else [],
            "index": corr_df.index.tolist() if not corr_df.empty else [],
            "values": corr_df.values.tolist() if not corr_df.empty else []
        }
    }


@app.get("/api/analytics/performance")
def get_performance_analysis(
    low_threshold: Optional[float] = None,
    high_threshold: Optional[float] = None,
    low_thresh: float = 2.0,
    mod_thresh: float = 4.0
):
    df = get_all_students()
    if df.empty:
        return {
            "low_usage": {"count": 0, "avg_marks": 0.0, "avg_study": 0.0, "pass_rate": 0.0, "tier_label": "Low Usage"},
            "moderate_usage": {"count": 0, "avg_marks": 0.0, "avg_study": 0.0, "pass_rate": 0.0, "tier_label": "Moderate Usage"},
            "high_usage": {"count": 0, "avg_marks": 0.0, "avg_study": 0.0, "pass_rate": 0.0, "tier_label": "High Usage"},
            "chart_data": {"categories": [], "avg_marks": [], "counts": [], "pass_rates": []},
            "groups": []
        }

    lt = low_threshold if low_threshold is not None else low_thresh
    ht = high_threshold if high_threshold is not None else mod_thresh

    low_df = df[df["social_media_hours"] < lt]
    mod_df = df[(df["social_media_hours"] >= lt) & (df["social_media_hours"] <= ht)]
    high_df = df[df["social_media_hours"] > ht]

    def calc_metrics(sub_df, label):
        if sub_df.empty:
            return {"count": 0, "avg_marks": 0.0, "avg_study": 0.0, "pass_rate": 0.0, "tier_label": label}
        count = len(sub_df)
        avg_m = round(float(sub_df["academic_marks"].mean()), 2)
        avg_st = round(float(sub_df["study_hours"].mean()), 2)
        pass_count = len(sub_df[sub_df["academic_marks"] >= 50.0])
        pass_rate = round(float(pass_count / count * 100), 1)
        return {
            "count": count,
            "avg_marks": avg_m,
            "avg_study": avg_st,
            "pass_rate": pass_rate,
            "tier_label": label
        }

    low_metrics = calc_metrics(low_df, f"Low (<{lt}h)")
    mod_metrics = calc_metrics(mod_df, f"Moderate ({lt}-{ht}h)")
    high_metrics = calc_metrics(high_df, f"High (>{ht}h)")

    df_cat = categorize_usage(df, lt, ht)
    grouped = df_cat.groupby("usage_group").agg(
        student_count=("student_id", "count"),
        mean_marks=("academic_marks", "mean"),
        median_marks=("academic_marks", "median"),
        mean_study_hours=("study_hours", "mean"),
        mean_sleep_hours=("sleep_hours", "mean"),
        mean_attendance=("attendance", "mean")
    ).reset_index()

    group_order = [f"Low (<{lt}h)", f"Moderate ({lt}-{ht}h)", f"High (>{ht}h)"]
    grouped["order"] = grouped["usage_group"].apply(lambda x: group_order.index(x) if x in group_order else 99)
    grouped = grouped.sort_values("order").drop(columns=["order"])

    records = grouped.to_dict(orient="records")

    categories = [low_metrics["tier_label"], mod_metrics["tier_label"], high_metrics["tier_label"]]
    avg_marks = [low_metrics["avg_marks"], mod_metrics["avg_marks"], high_metrics["avg_marks"]]
    counts = [low_metrics["count"], mod_metrics["count"], high_metrics["count"]]
    pass_rates = [low_metrics["pass_rate"], mod_metrics["pass_rate"], high_metrics["pass_rate"]]

    return {
        "low_usage": low_metrics,
        "moderate_usage": mod_metrics,
        "high_usage": high_metrics,
        "chart_data": {
            "categories": categories,
            "avg_marks": avg_marks,
            "counts": counts,
            "pass_rates": pass_rates
        },
        "thresholds": {"low": lt, "moderate": ht},
        "groups": records
    }


@app.post("/api/report/pdf")
def generate_pdf_report(meta: ReportMetadata):
    df = get_all_students()
    if df.empty:
        raise HTTPException(status_code=400, detail="Cannot generate report from empty dataset.")

    temp_dir = tempfile.gettempdir()
    pdf_filename = f"StudyMetrics_Research_Report.pdf"
    pdf_path = os.path.join(temp_dir, pdf_filename)

    meta_dict = meta.dict()
    success, msg = build_pdf_report(df, meta_dict, pdf_path)

    if not success or not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail=f"PDF Generation failed: {msg}")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="StudyMetrics_Research_Report.pdf"
    )
