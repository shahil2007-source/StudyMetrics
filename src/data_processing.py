import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "student_id", "age", "gender", "course",
    "social_media_hours", "study_hours", "academic_marks",
    "platform", "sleep_hours", "attendance"
]


def validate_student_data(record: dict) -> tuple[bool, str]:
    """
    Validates student record according to required business constraints:
    - social_media_hours between 0 and 24
    - study_hours between 0 and 24
    - academic_marks between 0 and 100
    - attendance between 0 and 100
    - student_id not empty
    """
    try:
        student_id = str(record.get("student_id", record.get("Student_ID", ""))).strip()
        if not student_id:
            return False, "Student ID cannot be empty."

        age_val = record.get("age")
        age = float(age_val) if age_val is not None else 20.0
        if age < 15 or age > 100:
            return False, "Age must be between 15 and 100."

        sm_val = record.get("social_media_hours", record.get("Social_Media_Usage_Hours"))
        sm = float(sm_val) if sm_val is not None else 0.0
        if sm < 0.0 or sm > 24.0:
            return False, f"Social media usage ({sm} hrs) must be between 0 and 24 hours."

        sh_val = record.get("study_hours", record.get("Study_Hours"))
        sh = float(sh_val) if sh_val is not None else 0.0
        if sh < 0.0 or sh > 24.0:
            return False, f"Study hours ({sh} hrs) must be between 0 and 24 hours."

        marks_val = record.get("academic_marks", record.get("Academic_Marks"))
        marks = float(marks_val) if marks_val is not None else 0.0
        if marks < 0.0 or marks > 100.0:
            return False, f"Academic marks ({marks}%) must be between 0 and 100."

        att_val = record.get("attendance")
        att = float(att_val) if att_val is not None else 85.0
        if att < 0.0 or att > 100.0:
            return False, f"Attendance ({att}%) must be between 0 and 100."

        sleep_val = record.get("sleep_hours")
        sleep = float(sleep_val) if sleep_val is not None else 7.5
        if sleep < 0.0 or sleep > 24.0:
            return False, f"Sleep duration ({sleep} hrs) must be between 0 and 24 hours."

        return True, "Valid"
    except (ValueError, TypeError) as e:
        return False, f"Invalid numeric entry format: {str(e)}"


def process_uploaded_csv(uploaded_file) -> tuple[pd.DataFrame, list[str]]:
    """
    Reads, validates, and cleans an uploaded CSV file.
    Returns (cleaned_dataframe, error_messages_list).
    """
    errors = []
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return pd.DataFrame(), [f"Failed to read CSV file: {str(e)}"]

    # Check for missing required columns
    df.columns = [c.strip().lower() for c in df.columns]
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        return pd.DataFrame(), [f"CSV is missing required columns: {', '.join(missing_cols)}"]

    # Coerce numeric columns
    numeric_cols = ["age", "social_media_hours", "study_hours", "academic_marks", "sleep_hours", "attendance"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop fully null or invalid ID rows
    initial_len = len(df)
    df = df.dropna(subset=["student_id"] + numeric_cols).copy()
    dropped = initial_len - len(df)
    if dropped > 0:
        errors.append(f"Dropped {dropped} row(s) with missing or non-numeric values.")

    # Range validations
    valid_mask = (
        (df["social_media_hours"] >= 0) & (df["social_media_hours"] <= 24) &
        (df["study_hours"] >= 0) & (df["study_hours"] <= 24) &
        (df["academic_marks"] >= 0) & (df["academic_marks"] <= 100) &
        (df["attendance"] >= 0) & (df["attendance"] <= 100) &
        (df["sleep_hours"] >= 0) & (df["sleep_hours"] <= 24)
    )
    invalid_rows = len(df) - valid_mask.sum()
    if invalid_rows > 0:
        errors.append(f"Filtered out {invalid_rows} row(s) exceeding realistic numerical bounds (e.g. >24h or >100%).")
    
    df = df[valid_mask].copy()

    # Deduplicate student_id
    df["student_id"] = df["student_id"].astype(str).str.strip()
    dup_count = df.duplicated(subset=["student_id"]).sum()
    if dup_count > 0:
        errors.append(f"Removed {dup_count} duplicate Student ID(s).")
        df = df.drop_duplicates(subset=["student_id"], keep='first').copy()

    return df, errors


def filter_dataframe(
    df: pd.DataFrame,
    selected_courses: list = None,
    selected_genders: list = None,
    selected_platforms: list = None,
    sm_hours_range: tuple = (0.0, 24.0)
) -> pd.DataFrame:
    """Applies interactive sidebar filters to student dataframe."""
    if df.empty:
        return df

    filtered_df = df.copy()

    if selected_courses and "All" not in selected_courses:
        filtered_df = filtered_df[filtered_df["course"].isin(selected_courses)]

    if selected_genders and "All" not in selected_genders:
        filtered_df = filtered_df[filtered_df["gender"].isin(selected_genders)]

    if selected_platforms and "All" not in selected_platforms:
        filtered_df = filtered_df[filtered_df["platform"].isin(selected_platforms)]

    if sm_hours_range:
        min_sm, max_sm = sm_hours_range
        filtered_df = filtered_df[
            (filtered_df["social_media_hours"] >= min_sm) &
            (filtered_df["social_media_hours"] <= max_sm)
        ]

    return filtered_df


def categorize_usage(df: pd.DataFrame, low_threshold: float = 2.0, mod_threshold: float = 4.0) -> pd.DataFrame:
    """
    Categorizes social media usage into Low, Moderate, High groups based on configurable thresholds.
    """
    if df.empty or "social_media_hours" not in df.columns:
        return df

    df_cat = df.copy()

    def get_group(hrs):
        if pd.isna(hrs):
            return "Unknown"
        if hrs < low_threshold:
            return f"Low (<{low_threshold}h)"
        elif hrs <= mod_threshold:
            return f"Moderate ({low_threshold}-{mod_threshold}h)"
        else:
            return f"High (>{mod_threshold}h)"

    df_cat["usage_group"] = df_cat["social_media_hours"].apply(get_group)
    return df_cat
