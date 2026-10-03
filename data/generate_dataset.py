import numpy as np
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)

n_samples = 120

student_ids = [f"STU{1001 + i}" for i in range(n_samples)]
ages = np.random.randint(18, 26, size=n_samples)

genders = np.random.choice(
    ["Female", "Male", "Non-Binary", "Prefer not to say"],
    size=n_samples,
    p=[0.48, 0.46, 0.04, 0.02]
)

courses = np.random.choice(
    [
        "Computer Science",
        "Business Administration",
        "Engineering",
        "Psychology",
        "Mathematics",
        "Data Science",
        "Medicine",
        "Arts & Design"
    ],
    size=n_samples
)

platforms = np.random.choice(
    ["Instagram", "TikTok", "YouTube", "X (Twitter)", "Snapchat", "Reddit", "LinkedIn"],
    size=n_samples,
    p=[0.30, 0.25, 0.20, 0.08, 0.07, 0.06, 0.04]
)

# Generating correlated synthetic metrics:
social_media = np.random.normal(loc=3.5, scale=1.4, size=n_samples)
social_media = np.clip(social_media, 0.5, 9.0)

study_hours = 8.5 - (0.5 * social_media) + np.random.normal(0, 1.2, size=n_samples)
study_hours = np.clip(study_hours, 1.0, 11.0)

sleep_hours = 8.0 - (0.25 * social_media) + np.random.normal(0, 0.8, size=n_samples)
sleep_hours = np.clip(sleep_hours, 4.5, 9.5)

attendance = 70.0 + (3.0 * study_hours) - (1.5 * social_media) + np.random.normal(0, 5.0, size=n_samples)
attendance = np.clip(attendance, 60.0, 100.0)

academic_marks = 45.0 + (3.8 * study_hours) + (0.2 * attendance) + (1.2 * sleep_hours) - (2.1 * social_media) + np.random.normal(0, 4.5, size=n_samples)
academic_marks = np.clip(academic_marks, 42.0, 98.5)

df = pd.DataFrame({
    "student_id": student_ids,
    "age": ages,
    "gender": genders,
    "course": courses,
    "social_media_hours": np.round(social_media, 1),
    "study_hours": np.round(study_hours, 1),
    "academic_marks": np.round(academic_marks, 1),
    "platform": platforms,
    "sleep_hours": np.round(sleep_hours, 1),
    "attendance": np.round(attendance, 1)
})

df.to_csv("/Users/tankalashahilkumar/Desktop/maths/data/sample_students.csv", index=False)
print(f"Dataset generated successfully with {len(df)} records!")
