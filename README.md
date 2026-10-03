# StudyMetrics 2.0 - Student Analytics Platform (Full-Stack Next.js + FastAPI)

StudyMetrics is an end-to-end full-stack analytics platform built with **Next.js**, **React**, **FastAPI (Python)**, **MongoDB Atlas**, **Plotly.js**, and **ReportLab**. It provides quantitative correlation analysis and statistical modeling between social media usage, study hours, and academic performance among students.

---

## 🌟 Architecture & Technology Stack

- **Frontend**: Next.js 14 (App Router), React 18, Tailwind CSS, Lucide Icons, Plotly.js (`react-plotly.js`)
- **Backend**: Python FastAPI (Serverless compatible with Vercel)
- **Data Engine**: Pandas, NumPy, SciPy, Scikit-learn
- **Database**: MongoDB Atlas with automatic **CSV Fallback** (`data/sample_students.csv`)
- **Reporting**: ReportLab PDF Generation Engine
- **Deployment**: Vercel

---

## 🚀 Key Pages & Features

1. **Dashboard**: 5 Key KPI cards (Total Students, Avg Social Media, Avg Study Hours, Avg Marks, Pearson r), interactive scatter plots with regression trendlines, and executive statistical summary.
2. **Student Data Management**: Complete CRUD operations, real-time search, usage tier filtering, modal forms, CSV file import/upload, and CSV export.
3. **Statistical Analysis**: Pearson & Spearman rank correlation cards, p-values, descriptive statistics table (mean, std, quartiles, IQR), and interactive correlation heatmap.
4. **Data Visualization**: Multi-dimensional interactive Plotly charts including 2D scatter plots, 3D scatter plots, and grade distribution histograms.
5. **Performance Analysis**: Cohort usage breakdown (Low, Moderate, High risk tiers) with interactive cutoff sliders and recommended academic interventions.
6. **Research Report Generator**: Custom metadata input form, report structure preview, and one-click ReportLab PDF report generation and download.

---

## 💻 Local Development Setup

### 1. Prerequisites
- **Node.js**: v18.x or higher
- **Python**: v3.9 or higher

### 2. Installation & Setup

1. **Clone the repository and install Node.js dependencies**:
   ```bash
   npm install
   ```

2. **Install Python backend dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables (Optional)**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   *Note: If `MONGODB_URI` is not set, StudyMetrics automatically uses local CSV storage (`data/sample_students.csv`).*

### 3. Running the Application Locally

#### Option A: Concurrent Development (Recommended)

1. **Start the FastAPI backend server** (Port 8000):
   ```bash
   npm run fastapi-dev
   # Or manually:
   python3 -m uvicorn api.index:app --reload --port 8000
   ```

2. **In a separate terminal, start the Next.js frontend** (Port 3000):
   ```bash
   npm run dev
   ```

3. Open **`http://localhost:3000`** in your browser.

---

## ☁️ Deploying to Vercel

### Step 1: Push Code to GitHub / Git Repository
```bash
git add .
git commit -m "Deploy full-stack StudyMetrics app to Vercel"
git push origin main
```

### Step 2: Deploy via Vercel CLI or Dashboard

#### Option A: Vercel Dashboard (Recommended)
1. Log into your [Vercel Dashboard](https://vercel.com).
2. Click **Add New** > **Project** and select your GitHub repository.
3. Vercel will automatically detect `vercel.json` and configure:
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
4. Add your Environment Variables under Project Settings > Environment Variables:
   - `MONGODB_URI`: *Your MongoDB connection string*
   - `MONGODB_DB_NAME`: `studymetrics`
   - `MONGODB_COLLECTION`: `students`
5. Click **Deploy**.

#### Option B: Vercel CLI
```bash
npm i -g vercel
vercel
```

---

## 🔒 Environment Security & Fallback
- MongoDB credentials are read securely via environment variables (`MONGODB_URI`) and are **never exposed** to the frontend.
- When MongoDB credentials are absent or unreachable, the application gracefully operates using the local CSV fallback data engine (`data/sample_students.csv`).
