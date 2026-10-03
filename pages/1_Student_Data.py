import os
import sys
import textwrap
import streamlit as st
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import (
    get_all_students,
    add_student_record,
    update_student_record,
    delete_student_record,
    save_all_students
)
from src.data_processing import validate_student_data, process_uploaded_csv

st.html(textwrap.dedent("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 2rem; color: #111827; margin: 0 0 0.25rem 0;">📋 Student Data Management</h1>
        <p style="color: #64748B; font-size: 1rem; margin: 0;">Add, edit, delete, search, upload CSV datasets, and manage student records.</p>
    </div>
"""))

df = get_all_students()

# Tabs for CRUD operations and File I/O
tab_view, tab_add, tab_edit, tab_csv = st.tabs([
    "🔍 View & Search",
    "➕ Add Student",
    "✏️ Edit / Delete",
    "📁 CSV Import & Export"
])

# ----------------- TAB 1: VIEW & SEARCH -----------------
with tab_view:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="saas-card-header">
                <div class="saas-card-title">🔍 Search & Filter Student Records</div>
            </div>
        """))
        
        col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
        with col_s1:
            search_query = st.text_input("Search Student ID, Course, or Platform:", "").strip()
        with col_s2:
            course_filter = st.selectbox("Course Filter:", ["All"] + sorted(df["course"].unique().tolist()) if not df.empty else ["All"])
        with col_s3:
            gender_filter = st.selectbox("Gender Filter:", ["All"] + sorted(df["gender"].unique().tolist()) if not df.empty else ["All"])

        display_df = df.copy()
        
        if search_query:
            display_df = display_df[
                display_df["student_id"].astype(str).str.contains(search_query, case=False, na=False) |
                display_df["course"].astype(str).str.contains(search_query, case=False, na=False) |
                display_df["platform"].astype(str).str.contains(search_query, case=False, na=False)
            ]

        if course_filter != "All":
            display_df = display_df[display_df["course"] == course_filter]

        if gender_filter != "All":
            display_df = display_df[display_df["gender"] == gender_filter]

        st.markdown(f"**Showing {len(display_df)} of {len(df)} total records:**")
        st.dataframe(display_df, use_container_width=True, hide_index=True)


# ----------------- TAB 2: ADD STUDENT -----------------
with tab_add:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="saas-card-header">
                <div class="saas-card-title">➕ Add New Student Record</div>
                <div class="saas-card-sub">Form validation enforces bounds: 0-24h usage, 0-100% marks, unique student ID</div>
            </div>
        """))

        with st.form("add_student_form", clear_on_submit=True):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                new_id = st.text_input("Student ID (e.g. STU1201)*", "").strip()
                new_age = st.number_input("Age*", min_value=15, max_value=100, value=20)
                new_gender = st.selectbox("Gender", ["Female", "Male", "Non-Binary", "Prefer not to say"])
            
            with f_col2:
                new_course = st.selectbox("Course*", [
                    "Computer Science", "Business Administration", "Engineering",
                    "Psychology", "Mathematics", "Data Science", "Medicine", "Arts & Design"
                ])
                new_platform = st.selectbox("Primary Platform*", [
                    "Instagram", "TikTok", "YouTube", "X (Twitter)", "Snapchat", "Reddit", "LinkedIn"
                ])
                new_attendance = st.number_input("Attendance (%)*", min_value=0.0, max_value=100.0, value=85.0, step=0.5)

            with f_col3:
                new_sm = st.number_input("Social Media Usage (Hours)*", min_value=0.0, max_value=24.0, value=3.0, step=0.5)
                new_study = st.number_input("Daily Study Hours*", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
                new_marks = st.number_input("Academic Marks (%)*", min_value=0.0, max_value=100.0, value=75.0, step=0.5)
                new_sleep = st.number_input("Sleep Duration (Hours)", min_value=0.0, max_value=24.0, value=7.5, step=0.5)

            submitted = st.form_submit_button("💾 Save Student Record", type="primary", use_container_width=True)

            if submitted:
                record_dict = {
                    "student_id": new_id,
                    "age": new_age,
                    "gender": new_gender,
                    "course": new_course,
                    "social_media_hours": new_sm,
                    "study_hours": new_study,
                    "academic_marks": new_marks,
                    "platform": new_platform,
                    "sleep_hours": new_sleep,
                    "attendance": new_attendance
                }

                valid, msg = validate_student_data(record_dict)
                if not valid:
                    st.error(f"❌ Validation Error: {msg}")
                else:
                    success, db_msg = add_student_record(record_dict)
                    if success:
                        st.success(f"✅ {db_msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ Database Error: {db_msg}")


# ----------------- TAB 3: EDIT / DELETE -----------------
with tab_edit:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="saas-card-header">
                <div class="saas-card-title">✏️ Modify or Remove Student Record</div>
            </div>
        """))
        
        if df.empty:
            st.info("No records available to edit.")
        else:
            student_list = df["student_id"].astype(str).tolist()
            selected_id = st.selectbox("Select Student ID:", student_list)

            curr_row = df[df["student_id"].astype(str) == selected_id].iloc[0]

            e_col1, e_col2, e_col3 = st.columns(3)
            with e_col1:
                e_age = st.number_input("Age", min_value=15, max_value=100, value=int(curr_row["age"]), key="e_age")
                e_gender = st.selectbox("Gender", ["Female", "Male", "Non-Binary", "Prefer not to say"], 
                                        index=["Female", "Male", "Non-Binary", "Prefer not to say"].index(curr_row["gender"]) if curr_row["gender"] in ["Female", "Male", "Non-Binary", "Prefer not to say"] else 0, key="e_gen")
                e_course = st.text_input("Course", value=str(curr_row["course"]), key="e_course")

            with e_col2:
                e_platform = st.text_input("Platform", value=str(curr_row["platform"]), key="e_plat")
                e_attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=float(curr_row["attendance"]), key="e_att")
                e_sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=float(curr_row["sleep_hours"]), key="e_sleep")

            with e_col3:
                e_sm = st.number_input("Social Media Hours", min_value=0.0, max_value=24.0, value=float(curr_row["social_media_hours"]), key="e_sm")
                e_study = st.number_input("Study Hours", min_value=0.0, max_value=24.0, value=float(curr_row["study_hours"]), key="e_study")
                e_marks = st.number_input("Academic Marks (%)", min_value=0.0, max_value=100.0, value=float(curr_row["academic_marks"]), key="e_marks")

            btn_cols = st.columns(2)
            with btn_cols[0]:
                if st.button("✏️ Save Changes", type="primary", use_container_width=True):
                    updated_dict = {
                        "student_id": selected_id,
                        "age": e_age,
                        "gender": e_gender,
                        "course": e_course,
                        "social_media_hours": e_sm,
                        "study_hours": e_study,
                        "academic_marks": e_marks,
                        "platform": e_platform,
                        "sleep_hours": e_sleep,
                        "attendance": e_attendance
                    }
                    valid, msg = validate_student_data(updated_dict)
                    if not valid:
                        st.error(f"❌ {msg}")
                    else:
                        success, db_msg = update_student_record(selected_id, updated_dict)
                        if success:
                            st.success(f"✅ {db_msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {db_msg}")

            with btn_cols[1]:
                if st.button("🗑️ Delete Record", use_container_width=True):
                    success, db_msg = delete_student_record(selected_id)
                    if success:
                        st.success(f"✅ {db_msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {db_msg}")


# ----------------- TAB 4: CSV IMPORT / EXPORT -----------------
with tab_csv:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="saas-card-header">
                <div class="saas-card-title">📁 Import & Export Datasets</div>
                <div class="saas-card-sub">Upload CSV datasets or download active data</div>
            </div>
        """))

        uploaded_file = st.file_uploader("Upload CSV file:", type=["csv"])

        if uploaded_file is not None:
            cleaned_df, msgs = process_uploaded_csv(uploaded_file)
            for m in msgs:
                st.info(f"ℹ️ {m}")

            if not cleaned_df.empty:
                st.write(f"Previewing Uploaded Data ({len(cleaned_df)} valid records):")
                st.dataframe(cleaned_df.head(10), use_container_width=True)

                mode_cols = st.columns(2)
                with mode_cols[0]:
                    if st.button("🔄 Overwrite Entire Database", type="primary", use_container_width=True):
                        save_all_students(cleaned_df)
                        st.success("✅ Database successfully overwritten!")
                        st.rerun()
                
                with mode_cols[1]:
                    if st.button("➕ Append Records to Data", use_container_width=True):
                        existing = get_all_students()
                        combined = pd.concat([existing, cleaned_df], ignore_index=True).drop_duplicates(subset=["student_id"])
                        save_all_students(combined)
                        st.success("✅ Records successfully appended!")
                        st.rerun()

        st.markdown("---")
        st.subheader("Download Current Dataset")
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Dataset (CSV)",
            data=csv_bytes,
            file_name="studymetrics_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )
