import os
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
DB_NAME = os.getenv("MONGODB_DB_NAME", "studymetrics")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "students")
LOCAL_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_students.csv")

_mongo_client = None
_mongo_db = None
_mongo_collection = None
_is_connected = False


def check_mongodb_connection():
    """Attempts to connect to MongoDB Atlas and test ping."""
    global _mongo_client, _mongo_db, _mongo_collection, _is_connected
    if not MONGODB_URI:
        _is_connected = False
        return False, "MONGODB_URI environment variable not configured. Using CSV fallback."
    
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

        _mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2500)
        # Verify connection
        _mongo_client.admin.command('ping')
        _mongo_db = _mongo_client[DB_NAME]
        _mongo_collection = _mongo_db[COLLECTION_NAME]
        _is_connected = True
        return True, "Connected successfully to MongoDB Atlas."
    except Exception as e:
        _is_connected = False
        _mongo_client = None
        return False, f"MongoDB connection failed ({str(e)}). Operating in CSV fallback mode."


def is_mongodb_connected():
    """Returns whether MongoDB is currently active."""
    global _is_connected
    return _is_connected


def get_all_students() -> pd.DataFrame:
    """Fetch all student records from MongoDB if connected, else from local CSV."""
    global _is_connected, _mongo_collection
    
    if _is_connected and _mongo_collection is not None:
        try:
            records = list(_mongo_collection.find({}, {'_id': 0}))
            if records:
                df = pd.DataFrame(records)
                return df
            else:
                # If collection is empty, load sample CSV and populate MongoDB
                df = load_local_csv()
                if not df.empty:
                    save_all_students(df)
                return df
        except Exception as e:
            print(f"Error fetching from MongoDB: {e}")
            return load_local_csv()
    else:
        return load_local_csv()


def load_local_csv() -> pd.DataFrame:
    """Load local CSV file."""
    if os.path.exists(LOCAL_CSV_PATH):
        try:
            df = pd.read_csv(LOCAL_CSV_PATH)
            return df
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


def save_local_csv(df: pd.DataFrame):
    """Save dataframe to local CSV."""
    os.makedirs(os.path.dirname(LOCAL_CSV_PATH), exist_ok=True)
    df.to_csv(LOCAL_CSV_PATH, index=False)


def save_all_students(df: pd.DataFrame) -> bool:
    """Overwrite all student records in DB or CSV."""
    global _is_connected, _mongo_collection
    
    records = df.to_dict('records')
    save_local_csv(df)
    
    if _is_connected and _mongo_collection is not None:
        try:
            _mongo_collection.delete_many({})
            if records:
                _mongo_collection.insert_many(records)
            return True
        except Exception as e:
            print(f"MongoDB batch write failed: {e}")
            return False
    return True


def add_student_record(record: dict) -> tuple[bool, str]:
    """Add a single student record with validation against duplicate student_id."""
    df = get_all_students()
    student_id = record.get("student_id")
    
    if not student_id:
        return False, "Student ID cannot be empty."
        
    if not df.empty and student_id in df["student_id"].astype(str).values:
        return False, f"Student ID '{student_id}' already exists in database."

    # Standardize types
    record_clean = {
        "student_id": str(record["student_id"]).strip(),
        "age": int(record["age"]),
        "gender": str(record.get("gender", "Prefer not to say")),
        "course": str(record.get("course", "General")),
        "social_media_hours": float(record["social_media_hours"]),
        "study_hours": float(record["study_hours"]),
        "academic_marks": float(record["academic_marks"]),
        "platform": str(record.get("platform", "Instagram")),
        "sleep_hours": float(record.get("sleep_hours", 7.0)),
        "attendance": float(record.get("attendance", 85.0))
    }
    
    if _is_connected and _mongo_collection is not None:
        try:
            _mongo_collection.insert_one(record_clean.copy())
        except Exception as e:
            print(f"MongoDB insert error: {e}")
    
    # Also update CSV/memory fallback
    if df.empty:
        new_df = pd.DataFrame([record_clean])
    else:
        new_df = pd.concat([df, pd.DataFrame([record_clean])], ignore_index=True)
        
    save_local_csv(new_df)
    return True, f"Student record {student_id} added successfully!"


def update_student_record(student_id: str, updated_record: dict) -> tuple[bool, str]:
    """Update an existing student record."""
    df = get_all_students()
    if df.empty or student_id not in df["student_id"].astype(str).values:
        return False, f"Student ID '{student_id}' not found."

    record_clean = {
        "student_id": str(student_id).strip(),
        "age": int(updated_record["age"]),
        "gender": str(updated_record.get("gender", "Prefer not to say")),
        "course": str(updated_record.get("course", "General")),
        "social_media_hours": float(updated_record["social_media_hours"]),
        "study_hours": float(updated_record["study_hours"]),
        "academic_marks": float(updated_record["academic_marks"]),
        "platform": str(updated_record.get("platform", "Instagram")),
        "sleep_hours": float(updated_record.get("sleep_hours", 7.0)),
        "attendance": float(updated_record.get("attendance", 85.0))
    }

    if _is_connected and _mongo_collection is not None:
        try:
            _mongo_collection.replace_one({"student_id": student_id}, record_clean, upsert=True)
        except Exception as e:
            print(f"MongoDB update error: {e}")

    # Update in DataFrame
    idx = df[df["student_id"].astype(str) == str(student_id)].index
    for col, val in record_clean.items():
        df.loc[idx, col] = val
        
    save_local_csv(df)
    return True, f"Student record {student_id} updated successfully!"


def delete_student_record(student_id: str) -> tuple[bool, str]:
    """Delete a student record by student_id."""
    df = get_all_students()
    if df.empty or str(student_id) not in df["student_id"].astype(str).values:
        return False, f"Student ID '{student_id}' not found."

    if _is_connected and _mongo_collection is not None:
        try:
            _mongo_collection.delete_one({"student_id": str(student_id)})
        except Exception as e:
            print(f"MongoDB delete error: {e}")

    new_df = df[df["student_id"].astype(str) != str(student_id)].reset_index(drop=True)
    save_local_csv(new_df)
    return True, f"Student record {student_id} deleted successfully."
