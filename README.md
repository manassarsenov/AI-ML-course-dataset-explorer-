# Dataset m - Dataset Explorer

A fast, lightweight dataset inspection tool built with Streamlit and pandas for the AI/ML course.

---

## 🎨 Theme & Appearance
- **App Name**: Dataset m
- **Main Accent Color**: `#0757ff` (headers, metrics, buttons)
- **Background Color**: `#f7faff` (soft blue canvas)

---

## ⚙️ Verified Environment & Versions
The app was verified on Windows 11 (AMD64) using the local virtual environment:
- **Python**: `3.13.14` (64-bit)
- **Interpreter Path**: `C:\Users\user\OneDrive\Desktop\AI-ML course\.venv\Scripts\python.exe`
- **Key Packages**:
  - `streamlit`: **1.66.1**
  - `pandas`: **3.0.6**
  - `numpy`: **2.5.4**
  - `matplotlib`: **3.11.2**
  - `scikit-learn`: **1.9.1**
  - `ipykernel`: **7.4.0**
  - `IPython`: **9.17.1**

---

## 🚀 Actual Setup & Restart Commands (PowerShell)

### First-Time Environment Setup (Already Completed):
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Restarting the App:
To start or restart the application on port `8501`:
```powershell
.\.venv\Scripts\streamlit.exe run app.py --server.port 8501
```
Or alternatively:
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8501
```

Once running, open your browser at:
👉 **http://localhost:8501**

---

## 📋 Features Included
1. **CSV Upload**: Supports UTF-8 encoded CSVs up to 5 MB with comma (`,`) or semicolon (`;`) separator selection.
2. **Dataset Overview**: Displays full row count, column count, extra duplicate rows count, and a preview of the first 100 rows.
3. **Column Information**: Table of all column names and pandas data types.
4. **Missing Values Analysis**: 
   - Table of missing cell counts and percentages per column with pandas missing-value rule explanations.
   - **Interactive Missing Rows Button**: Displays a filtered table of rows containing at least one missing cell without altering the original dataset.
5. **Category Sum Bar Chart**:
   - Interactive dropdowns for category column and numeric column.
   - Sum calculations performed on the full dataset without replacing missing numbers with zero.
   - Groups with all missing numbers display as **"No data"** (zero is avoided).
   - Rows with missing categories are reported separately in a warning notice.
   - Displays up to the top 20 categories sorted descending by total, with a clear notice when truncated.
   - A complete exact totals table for all categories beneath the chart with labeled axes.
   - Clear fallback message if no numeric columns exist in the file.
6. **Spaces-Only Cells Analysis**:
   - Counts cells containing strings of whitespace only per column and in total.
   - Optional checkbox to view only rows with spaces-only cells without changing the source table.
7. **Boxplot & Outlier Detection (IQR)**:
   - Interactive dropdown to select any numeric column.
   - Calculates Q1, Median (Q2), Q3, IQR, and 1.5 × IQR outlier thresholds ($[Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}]$).
   - Renders a clean horizontal boxplot styled with the application theme.
   - Identifies and displays unusual rows (outliers) in a dedicated interactive table.
8. **Dual Dataset Comparison & Record Matching**:
   - Two upload fields for Dataset A (Reference) and Dataset B (Comparison) with independent separator choices and 5 MB limits.
   - Comparison summary cards: row counts, column counts, common columns, and unique columns with delta indicators.
   - Schema & column differences: side-by-side data type comparison with match/mismatch indicators and unique column tables.
   - Record matching by primary key (`row_id`): key validation (nulls/duplicates), matched vs unmatched record counts, and detailed field value difference tables.
   - Preserves 100% of the original uploaded datasets without any modification or automatic cleaning.
9. **ML Experiment Comparison (Run A vs Run B)**:
   - Two JSON upload fields for Experiment Run A and Experiment Run B (with quick-load fixture button for course files).
   - Core classification metrics: F1-score, Precision, and Recall side-by-side with exact differences $(B − A)$ and relative change percentages.
   - Evaluation conditions consistency audit: checks whether dataset, split, evaluation split, features, target, positive class, threshold, and seed match, clearly reporting any different or missing conditions.
   - Model settings & hyperparameter diff table (e.g. regularization parameter $C$, model architecture, penalty).
   - Strictly neutral, objective reporting without picking an automated winner.
10. **Error Handling**: Friendly notices for empty files (0 bytes or blank lines), wrong encoding, and corrupt formats.

---

## 📁 Key Project Files to Keep
- `app.py`: Main application code
- `requirements.txt`: Python package dependencies
- `.streamlit/config.toml`: App theme colors and server configuration
- `checks.txt`: Comprehensive log of automated and manual verification checks
- `README.md`: Setup, restart instructions, and version records
