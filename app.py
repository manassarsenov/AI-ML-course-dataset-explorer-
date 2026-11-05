import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

# Page setup
st.set_page_config(page_title="Dataset m", layout="wide")

# Apply custom colors (Main color: #0757ff, Background color: #f7faff)
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #f7faff;
    }
    /* Headers and titles accent color */
    h1, h2, h3, .stMetricValue {
        color: #0757ff;
    }
    /* Primary buttons */
    .stButton > button {
        background-color: #0757ff !important;
        color: #ffffff !important;
        font-weight: 500;
        border-radius: 6px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #0043c7 !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Dataset m")
st.caption("A simple and reliable Dataset Explorer & Comparison Tool")

# Sidebar app info & guidance
st.sidebar.header("About Dataset m")
st.sidebar.markdown(
    """
    **Dataset m** supports three core workflows:

    - **📊 Single Dataset Explorer**: Comprehensive single CSV analysis, data types, missing & spaces-only values, category aggregation bar chart, and IQR outlier detection.
    - **🔍 Dataset Comparison & Matching**: Dual CSV comparison, schema & column diffs, and primary key (`row_id`) record matching with detailed field value diffs.
    - **🧪 ML Experiment Comparison**: Compare metrics (F1, Precision, Recall), model settings, and evaluation condition consistency between two ML experiment runs (JSON).
    """
)
st.sidebar.divider()
st.sidebar.caption("🔒 Original data and experiment files are preserved intact without any modifications.")

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

# Tab-based navigation
tab1, tab2, tab3 = st.tabs([
    "📊 Single Dataset Explorer",
    "🔍 Dataset Comparison & Matching",
    "🧪 ML Experiment Comparison"
])

# ==============================================================================
# TAB 1: SINGLE DATASET EXPLORER (100% Backwards Compatible)
# ==============================================================================
with tab1:
    st.header("Single Dataset Explorer")

    t1_col_sep, t1_col_up = st.columns([1, 2])
    with t1_col_sep:
        separator_option = st.radio(
            "Choose column separator:",
            options=[", (Comma)", "; (Semicolon)"],
            index=0,
            help="Select comma or semicolon based on your CSV file format.",
            key="tab1_separator"
        )
        separator = "," if "," in separator_option else ";"
    with t1_col_up:
        uploaded_file = st.file_uploader(
            "Upload CSV file (Max 5 MB)",
            type=["csv"],
            help="Only CSV files up to 5 MB are allowed.",
            key="tab1_file_uploader"
        )

    if uploaded_file is None:
        st.info("Please upload a CSV file above to begin exploring.")
    else:
        # 1. Check file size
        if uploaded_file.size > MAX_FILE_SIZE_BYTES:
            st.error(f"File size exceeds the 5 MB limit (Current size: {uploaded_file.size / (1024 * 1024):.2f} MB). Please upload a smaller file.")
        # 2. Check empty file
        elif uploaded_file.size == 0:
            st.error("The uploaded file is empty (0 bytes). Please upload a valid CSV file with data.")
        else:
            try:
                # Read CSV with UTF-8 encoding and user-selected separator
                df = pd.read_csv(uploaded_file, sep=separator, encoding="utf-8")

                # Check if dataframe is completely empty (no columns or no rows)
                if df.empty and len(df.columns) == 0:
                    st.warning("The file was read, but it contains no columns or data.")
                elif len(df) == 0:
                    st.warning("The file contains header columns, but has 0 rows of data.")
                    st.write(f"**Detected Columns ({len(df.columns)}):**", list(df.columns))
                else:
                    # Summary metrics
                    row_count = len(df)
                    col_count = len(df.columns)
                    extra_duplicates = int(df.duplicated().sum())

                    st.subheader("Dataset Overview")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Rows", f"{row_count:,}")
                    col2.metric("Total Columns", f"{col_count:,}")
                    col3.metric("Extra Duplicate Rows", f"{extra_duplicates:,}")

                    st.caption(
                        "Note: All calculations are computed on the full file without altering your source data."
                    )

                    st.divider()

                    # Preview first 100 rows
                    st.subheader("Data Preview (First 100 Rows)")
                    preview_count = min(100, row_count)
                    st.caption(f"Showing the first {preview_count} rows out of {row_count:,} total rows.")
                    st.dataframe(df.head(100))

                    st.divider()

                    # Columns and types
                    st.subheader("Column Names & Data Types")
                    col_types_df = pd.DataFrame({
                        "Column Name": df.columns,
                        "Pandas Data Type": [str(t) for t in df.dtypes]
                    })
                    st.dataframe(col_types_df, hide_index=True)

                    st.divider()

                    # Count cells whose value is a string made only of one or more spaces
                    def is_spaces_only(val):
                        return isinstance(val, str) and len(val) > 0 and val.isspace()

                    # Computed across the full table without altering source data
                    spaces_counts = {col: int(df[col].apply(is_spaces_only).sum()) for col in df.columns}
                    total_spaces_cells = sum(spaces_counts.values())

                    # Missing values analysis
                    st.subheader("Missing Values Analysis")
                    missing_counts = df.isna().sum()
                    missing_pct = (missing_counts / row_count * 100).round(2)

                    missing_df = pd.DataFrame({
                        "Column Name": df.columns,
                        "Missing Count (NaN)": missing_counts.values,
                        "Missing Percentage (%)": missing_pct.values,
                        "Spaces-Only Count": [spaces_counts[col] for col in df.columns]
                    })
                    st.dataframe(missing_df, hide_index=True)

                    # Explanation of missing value rules
                    st.info(
                        "**Missing-value rules used:**\n"
                        "- When reading the CSV, standard empty cells, empty strings, 'NaN', 'NA', 'null', and 'None' are treated as missing (`NaN`).\n"
                        "- Cells containing whitespace only or custom sentinel strings (such as '?' or 'N/A' if unquoted) may not be recognized as missing unless standard pandas NA indicators apply.\n"
                        "- Calculations are based on exact pandas `isna()` results across all rows."
                    )

                    st.divider()

                    # Separate Spaces-Only Cells Analysis
                    st.subheader("Spaces-Only Cells Analysis")
                    st.caption(
                        "Count of cells containing a string made only of one or more spaces. "
                        "Ordinary empty/NaN values, 0, and '0' are not included in this count."
                    )

                    st.metric("Total Spaces-Only Cells", f"{total_spaces_cells:,}")

                    spaces_df = pd.DataFrame({
                        "Column Name": df.columns,
                        "Spaces-Only Cells Count": [spaces_counts[col] for col in df.columns]
                    })
                    st.dataframe(spaces_df, hide_index=True)

                    # Optional view: Checkbox to show only rows with at least one cell made only of spaces
                    spaces_row_mask = df.map(is_spaces_only).any(axis=1)
                    spaces_rows_count = int(spaces_row_mask.sum())

                    show_spaces_rows = st.checkbox(
                        f"Show only rows with at least one spaces-only cell ({spaces_rows_count:,})",
                        key="chk_spaces_rows"
                    )

                    if show_spaces_rows:
                        if spaces_rows_count == 0:
                            st.info("No rows contain spaces-only cells in this dataset.")
                        else:
                            st.markdown(f"**Rows containing at least one spaces-only cell ({spaces_rows_count:,} of {row_count:,} total rows):**")
                            st.caption("Optional filtered view only — full original table, summary, and chart remain unchanged.")
                            st.dataframe(df[spaces_row_mask])

                    # Extra feature: Button to inspect rows containing at least one missing value
                    missing_rows_mask = df.isna().any(axis=1)
                    missing_rows_total = int(missing_rows_mask.sum())

                    if "show_missing_rows" not in st.session_state:
                        st.session_state.show_missing_rows = False

                    btn_label = "Hide Rows with Missing Values" if st.session_state.show_missing_rows else f"Show Rows with Missing Values ({missing_rows_total:,})"

                    if st.button(btn_label, key="btn_missing_rows"):
                        st.session_state.show_missing_rows = not st.session_state.show_missing_rows

                    if st.session_state.show_missing_rows:
                        if missing_rows_total == 0:
                            st.success("No rows contain missing values. Every row in this dataset is complete!")
                        else:
                            st.markdown(f"**Rows containing at least one missing value ({missing_rows_total:,} of {row_count:,} rows):**")
                            st.caption("Filtered display only — the original uploaded data remains completely unchanged.")
                            st.dataframe(df[missing_rows_mask])

                    st.divider()

                    # Duplicate rows explanation
                    st.subheader("Duplicate Rows Information")
                    if extra_duplicates == 0:
                        st.success("No duplicate rows found. Every row in this dataset is unique.")
                    else:
                        st.warning(
                            f"Found **{extra_duplicates:,} extra exact duplicate rows** (excluding each row's first occurrence). "
                            "Original data remains unchanged."
                        )

                    st.divider()

                    # --- Category Bar Chart Section ---
                    st.subheader("Category Sum Bar Chart")

                    # Detect usable numeric columns
                    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

                    if not numeric_cols:
                        st.info(
                            "**Chart unavailable:** There are no usable numeric columns in this dataset. "
                            "The bar chart requires at least one numeric column to compute category sums. "
                            "The dataset overview, preview, and column analysis above remain fully functional."
                        )
                    else:
                        st.caption("Select a category column and a numeric column to visualize the sum for each category.")
                        chart_col1, chart_col2 = st.columns(2)
                        with chart_col1:
                            selected_category = st.selectbox(
                                "Select Category Column:",
                                options=list(df.columns),
                                index=0,
                                help="Choose any column to group categories by.",
                                key="t1_selected_category"
                            )
                        with chart_col2:
                            selected_numeric = st.selectbox(
                                "Select Numeric Column:",
                                options=numeric_cols,
                                index=0,
                                help="Choose a numeric column to calculate the sum.",
                                key="t1_selected_numeric"
                            )

                        # 1. Report rows with a missing category separately
                        missing_cat_mask = df[selected_category].isna()
                        missing_cat_count = int(missing_cat_mask.sum())
                        if missing_cat_count > 0:
                            st.warning(
                                f"**Missing category notice:** There are **{missing_cat_count:,} row(s)** where `{selected_category}` is missing (`NaN` or empty). "
                                "These rows are reported separately and excluded from the category breakdown."
                            )

                        # 2. Filter to rows with valid categories for grouping
                        valid_cat_df = df[~missing_cat_mask]

                        if valid_cat_df.empty:
                            st.warning("All rows in this dataset have a missing category value. No categories to display.")
                        else:
                            # Group by category, calculating sum with min_count=1
                            # min_count=1 ensures that if all numbers in a group are missing/NaN, the sum is NaN rather than 0
                            category_sums = valid_cat_df.groupby(selected_category)[selected_numeric].agg(lambda s: s.sum(min_count=1))

                            # Sort by total descending (NaN/missing totals placed last)
                            sorted_totals = category_sums.sort_values(ascending=False, na_position="last")
                            total_categories = len(sorted_totals)

                            # Top 20 categories for the chart
                            top20_totals = sorted_totals.head(20)

                            if total_categories > 20:
                                st.info(
                                    f"The chart below displays only the **top 20 categories** (out of {total_categories:,} total categories), "
                                    "sorted by total. The table below lists the exact totals for **all** categories."
                                )
                            else:
                                st.caption(f"Showing all {total_categories} categories sorted by total.")

                            # Prepare chart dataframe (only categories with non-null sums can be plotted)
                            chart_series = top20_totals.dropna()

                            if chart_series.empty:
                                st.info("No numeric values available to display in the chart (all selected category values are missing).")
                            else:
                                chart_df = chart_series.reset_index()
                                chart_df.columns = [selected_category, f"Sum of {selected_numeric}"]
                                # Convert category to string so Streamlit renders a discrete categorical axis
                                chart_df[selected_category] = chart_df[selected_category].astype(str)

                                st.bar_chart(
                                    data=chart_df,
                                    x=selected_category,
                                    y=f"Sum of {selected_numeric}",
                                    x_label=f"Category: {selected_category}",
                                    y_label=f"Aggregation: Sum of {selected_numeric}"
                                )

                            # Small table of all category totals below the chart
                            st.subheader("Category Exact Totals")
                            st.caption("Exact totals for all categories calculated across the full dataset:")

                            def format_display_total(val):
                                if pd.isna(val):
                                    return "No data"
                                if isinstance(val, (int, np.integer)) or (isinstance(val, (float, np.floating)) and float(val).is_integer()):
                                    return f"{int(val):,}"
                                return f"{val:,.4f}".rstrip("0").rstrip(".")

                            # Build display table with ALL categories
                            table_df = sorted_totals.reset_index()
                            table_df.columns = [f"Category ({selected_category})", f"Exact Sum ({selected_numeric})"]
                            table_df[f"Exact Sum ({selected_numeric})"] = table_df[f"Exact Sum ({selected_numeric})"].apply(format_display_total)

                            st.dataframe(table_df, hide_index=True)

                    st.divider()

                    # --- Outlier Detection & Boxplot Analysis ---
                    st.subheader("Numeric Column Analysis: Boxplot & Outliers (IQR)")

                    if not numeric_cols:
                        st.info(
                            "**Boxplot & Outlier Analysis unavailable:** There are no usable numeric columns in this dataset."
                        )
                    else:
                        st.caption("Select a numeric column to calculate the Interquartile Range (IQR), plot a boxplot, and inspect unusual rows (outliers).")

                        selected_box_col = st.selectbox(
                            "Select Numeric Column for Boxplot & IQR Analysis:",
                            options=numeric_cols,
                            index=0,
                            key="selectbox_boxplot_col",
                            help="Choose a numeric column to calculate IQR boundaries and detect outliers."
                        )

                        clean_series = df[selected_box_col].dropna()

                        if clean_series.empty:
                            st.warning(f"All values in column `{selected_box_col}` are missing or empty.")
                        else:
                            q1 = float(clean_series.quantile(0.25))
                            q3 = float(clean_series.quantile(0.75))
                            iqr = q3 - q1
                            lower_bound = q1 - 1.5 * iqr
                            upper_bound = q3 + 1.5 * iqr
                            median_val = float(clean_series.median())

                            # Display IQR Metrics in columns
                            iqr_col1, iqr_col2, iqr_col3, iqr_col4, iqr_col5 = st.columns(5)
                            iqr_col1.metric("Q1 (25%)", f"{q1:,.4g}")
                            iqr_col2.metric("Median (Q2)", f"{median_val:,.4g}")
                            iqr_col3.metric("Q3 (75%)", f"{q3:,.4g}")
                            iqr_col4.metric("IQR", f"{iqr:,.4g}")
                            iqr_col5.metric("Outlier Bounds", f"[{lower_bound:,.4g}, {upper_bound:,.4g}]")

                            # Boxplot
                            fig, ax = plt.subplots(figsize=(9, 2.8))
                            fig.patch.set_facecolor('#f7faff')
                            ax.set_facecolor('#ffffff')

                            ax.boxplot(
                                clean_series,
                                orientation='horizontal',
                                patch_artist=True,
                                boxprops=dict(facecolor='#0757ff', color='#0757ff', alpha=0.7),
                                medianprops=dict(color='#ffaa00', linewidth=2),
                                whiskerprops=dict(color='#0757ff', linewidth=1.5),
                                capprops=dict(color='#0757ff', linewidth=1.5),
                                flierprops=dict(marker='o', markerfacecolor='#e11d48', markeredgecolor='none', markersize=6, alpha=0.6)
                            )
                            ax.set_title(f"Boxplot: {selected_box_col}", color="#0757ff", fontsize=12, fontweight='bold')
                            ax.set_xlabel(selected_box_col)
                            ax.grid(axis='x', linestyle='--', alpha=0.4)
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)

                            # Outlier detection table
                            outlier_mask = (df[selected_box_col] < lower_bound) | (df[selected_box_col] > upper_bound)
                            outlier_count = int(outlier_mask.sum())

                            st.subheader(f"Unusual Rows (Outliers in `{selected_box_col}`)")
                            st.caption(
                                f"Rows with `{selected_box_col}` < {lower_bound:,.4g} or `{selected_box_col}` > {upper_bound:,.4g} using the 1.5 × IQR rule."
                            )

                            if outlier_count == 0:
                                st.success(f"No unusual rows found for `{selected_box_col}` using the 1.5 × IQR rule.")
                            else:
                                st.warning(f"Found **{outlier_count:,} unusual row(s)** ({outlier_count / row_count * 100:.2f}% of all rows).")
                                st.dataframe(df[outlier_mask])

            except UnicodeDecodeError:
                st.error("Encoding Error: Could not read the file with UTF-8 encoding. Please save your CSV using UTF-8 encoding and try again.")
            except pd.errors.EmptyDataError:
                st.error("Empty Data Error: The file does not contain any readable columns or data.")
            except pd.errors.ParserError as pe:
                st.error(f"Parser Error: Could not parse CSV with separator '{separator}'. Check if the correct separator was chosen. Details: {pe}")
            except Exception as e:
                st.error(f"Cannot read file: An unexpected error occurred while reading the CSV ({type(e).__name__}: {e}).")


# ==============================================================================
# TAB 2: DATASET COMPARISON & MATCHING
# ==============================================================================
with tab2:
    st.header("Dataset Comparison & Matching")
    st.caption("Compare schema differences and perform record matching between two CSV datasets.")

    # Two Upload Fields
    col_up_a, col_up_b = st.columns(2)

    with col_up_a:
        st.subheader("Dataset A (Reference / Base)")
        sep_opt_a = st.radio(
            "Dataset A Separator:",
            options=[", (Comma)", "; (Semicolon)"],
            index=0,
            horizontal=True,
            key="tab2_sep_a"
        )
        sep_a = "," if "," in sep_opt_a else ";"
        file_a = st.file_uploader(
            "Upload Dataset A (Reference / Base CSV)",
            type=["csv"],
            key="tab2_file_a",
            help="Upload base/reference CSV (Max 5 MB)."
        )

    with col_up_b:
        st.subheader("Dataset B (Comparison / Target)")
        sep_opt_b = st.radio(
            "Dataset B Separator:",
            options=[", (Comma)", "; (Semicolon)"],
            index=0,
            horizontal=True,
            key="tab2_sep_b"
        )
        sep_b = "," if "," in sep_opt_b else ";"
        file_b = st.file_uploader(
            "Upload Dataset B (Comparison / Target CSV)",
            type=["csv"],
            key="tab2_file_b",
            help="Upload comparison/target CSV (Max 5 MB)."
        )

    if file_a is None or file_b is None:
        if file_a is None and file_b is None:
            st.info("Please upload both Dataset A (Reference) and Dataset B (Comparison) above to begin comparison and matching.")
        elif file_a is None:
            st.warning("Please upload Dataset A (Reference) to proceed with comparison.")
        else:
            st.warning("Please upload Dataset B (Comparison) to proceed with comparison.")
    else:
        # Check file sizes
        file_a_oversized = file_a.size > MAX_FILE_SIZE_BYTES
        file_b_oversized = file_b.size > MAX_FILE_SIZE_BYTES
        file_a_empty = file_a.size == 0
        file_b_empty = file_b.size == 0

        if file_a_oversized:
            st.error(f"Dataset A exceeds the 5 MB limit ({file_a.size / (1024 * 1024):.2f} MB). Please upload a smaller file.")
        if file_b_oversized:
            st.error(f"Dataset B exceeds the 5 MB limit ({file_b.size / (1024 * 1024):.2f} MB). Please upload a smaller file.")
        if file_a_empty:
            st.error("Dataset A is empty (0 bytes). Please upload a valid CSV file with data.")
        if file_b_empty:
            st.error("Dataset B is empty (0 bytes). Please upload a valid CSV file with data.")

        if not (file_a_oversized or file_b_oversized or file_a_empty or file_b_empty):
            df_a = None
            df_b = None

            try:
                df_a = pd.read_csv(file_a, sep=sep_a, encoding="utf-8")
            except UnicodeDecodeError:
                st.error("Encoding Error in Dataset A: UTF-8 encoding is required. Please save Dataset A using UTF-8.")
            except pd.errors.EmptyDataError:
                st.error("Empty Data Error in Dataset A: The file contains no readable columns or data.")
            except pd.errors.ParserError as pe:
                st.error(f"Parser Error in Dataset A with separator '{sep_a}': {pe}")
            except Exception as e:
                st.error(f"Error reading Dataset A ({type(e).__name__}: {e})")

            try:
                df_b = pd.read_csv(file_b, sep=sep_b, encoding="utf-8")
            except UnicodeDecodeError:
                st.error("Encoding Error in Dataset B: UTF-8 encoding is required. Please save Dataset B using UTF-8.")
            except pd.errors.EmptyDataError:
                st.error("Empty Data Error in Dataset B: The file contains no readable columns or data.")
            except pd.errors.ParserError as pe:
                st.error(f"Parser Error in Dataset B with separator '{sep_b}': {pe}")
            except Exception as e:
                st.error(f"Error reading Dataset B ({type(e).__name__}: {e})")

            if df_a is not None and df_b is not None:
                # Check empty conditions
                if df_a.empty and len(df_a.columns) == 0:
                    st.warning("Dataset A was read, but it contains no columns or data.")
                elif df_b.empty and len(df_b.columns) == 0:
                    st.warning("Dataset B was read, but it contains no columns or data.")
                else:
                    rows_a = len(df_a)
                    rows_b = len(df_b)
                    cols_a = list(df_a.columns)
                    cols_b = list(df_b.columns)
                    set_a = set(cols_a)
                    set_b = set(cols_b)

                    common_cols = [c for c in cols_a if c in set_b]
                    only_a_cols = [c for c in cols_a if c not in set_b]
                    only_b_cols = [c for c in cols_b if c not in set_a]

                    st.divider()

                    # Summary Cards (b)
                    st.subheader("Comparison Summary Overview")
                    sc1, sc2, sc3, sc4 = st.columns(4)
                    with sc1:
                        st.metric(
                            "Rows (Dataset A vs B)",
                            f"{rows_a:,} vs {rows_b:,}",
                            delta=f"{rows_b - rows_a:+d} in B" if rows_a != rows_b else "Equal",
                            help="Total number of rows in Dataset A compared to Dataset B"
                        )
                    with sc2:
                        st.metric(
                            "Columns (Dataset A vs B)",
                            f"{len(cols_a):,} vs {len(cols_b):,}",
                            delta=f"{len(cols_b) - len(cols_a):+d} in B" if len(cols_a) != len(cols_b) else "Equal",
                            help="Total column count in Dataset A compared to Dataset B"
                        )
                    with sc3:
                        st.metric(
                            "Common Columns Count",
                            f"{len(common_cols):,}",
                            help="Columns present in both Dataset A and Dataset B"
                        )
                    with sc4:
                        st.metric(
                            "Columns Only in A / Only in B",
                            f"{len(only_a_cols):,} / {len(only_b_cols):,}",
                            help="Columns unique to Dataset A vs unique to Dataset B"
                        )

                    st.caption("🔒 **Source Data Integrity**: Both datasets are evaluated in their original uploaded form without any modification or cleaning.")

                    # Expandable preview
                    with st.expander("👁️ Quick Preview: First 5 Rows of Both Datasets", expanded=False):
                        pv_col1, pv_col2 = st.columns(2)
                        with pv_col1:
                            st.markdown(f"**Dataset A Preview ({rows_a:,} rows, {len(cols_a):,} cols):**")
                            st.dataframe(df_a.head(5))
                        with pv_col2:
                            st.markdown(f"**Dataset B Preview ({rows_b:,} rows, {len(cols_b):,} cols):**")
                            st.dataframe(df_b.head(5))

                    st.divider()

                    # Column Differences (c)
                    st.subheader("Column Differences & Schema Comparison")

                    if common_cols:
                        common_types_data = []
                        mismatched_dtype_cols = []
                        for c in common_cols:
                            dtype_a = str(df_a[c].dtype)
                            dtype_b = str(df_b[c].dtype)
                            types_match = (dtype_a == dtype_b)
                            if not types_match:
                                mismatched_dtype_cols.append(c)
                            common_types_data.append({
                                "Common Column": c,
                                "Type in Dataset A": dtype_a,
                                "Type in Dataset B": dtype_b,
                                "Status": "✅ Match" if types_match else "⚠️ Mismatch"
                            })
                        common_types_df = pd.DataFrame(common_types_data)

                        st.markdown(f"**Columns Present in Both Datasets ({len(common_cols):,}):**")
                        if mismatched_dtype_cols:
                            st.warning(
                                f"⚠️ Found **{len(mismatched_dtype_cols)} common column(s)** with differing pandas data types between Dataset A and Dataset B: "
                                f"{', '.join(f'`{col}`' for col in mismatched_dtype_cols)}."
                            )
                        st.dataframe(common_types_df, hide_index=True)
                    else:
                        st.warning("⚠️ No common columns found between Dataset A and Dataset B.")

                    diff_col1, diff_col2 = st.columns(2)
                    with diff_col1:
                        st.markdown(f"**Columns Unique to Dataset A ({len(only_a_cols):,}):**")
                        if only_a_cols:
                            unique_a_df = pd.DataFrame({
                                "Column Name": only_a_cols,
                                "Data Type in A": [str(df_a[c].dtype) for c in only_a_cols]
                            })
                            st.dataframe(unique_a_df, hide_index=True)
                        else:
                            st.success("None — all columns in Dataset A also exist in Dataset B.")

                    with diff_col2:
                        st.markdown(f"**Columns Unique to Dataset B ({len(only_b_cols):,}):**")
                        if only_b_cols:
                            unique_b_df = pd.DataFrame({
                                "Column Name": only_b_cols,
                                "Data Type in B": [str(df_b[c].dtype) for c in only_b_cols]
                            })
                            st.dataframe(unique_b_df, hide_index=True)
                        else:
                            st.success("None — all columns in Dataset B also exist in Dataset A.")

                    st.divider()

                    # Record Matching using a valid row_id (d)
                    st.subheader("Record Matching by Key (row_id)")

                    if not common_cols:
                        st.info("Record matching is unavailable because there are no common columns between the two datasets.")
                    else:
                        id_candidates = ["row_id", "id", "ID", "Id", "Row_ID", "ROW_ID", "order_id", "Order ID", "Order_ID"]
                        default_idx = 0
                        for idx, c in enumerate(common_cols):
                            if c in id_candidates:
                                default_idx = idx
                                break

                        selected_id = st.selectbox(
                            "Select Key Column (`row_id` / ID) for Matching:",
                            options=common_cols,
                            index=default_idx,
                            help="Choose the common column that uniquely identifies each record in both datasets.",
                            key="tab2_selected_id"
                        )

                        # Validate row_id
                        nulls_a = int(df_a[selected_id].isna().sum())
                        nulls_b = int(df_b[selected_id].isna().sum())
                        dup_a = int(df_a[selected_id].duplicated().sum())
                        dup_b = int(df_b[selected_id].duplicated().sum())

                        is_valid_key = (nulls_a == 0 and nulls_b == 0 and dup_a == 0 and dup_b == 0)

                        st.markdown(f"**Key Validation for `{selected_id}`:**")
                        vcol1, vcol2, vcol3, vcol4 = st.columns(4)
                        vcol1.metric("Nulls in Dataset A", f"{nulls_a:,}")
                        vcol2.metric("Nulls in Dataset B", f"{nulls_b:,}")
                        vcol3.metric("Duplicates in Dataset A", f"{dup_a:,}")
                        vcol4.metric("Duplicates in Dataset B", f"{dup_b:,}")

                        if is_valid_key:
                            st.success(
                                f"✅ **Valid Unique Key:** Column `{selected_id}` has 0 nulls and 0 duplicates in both datasets. "
                                "It provides an unambiguous 1:1 record identifier."
                            )
                        else:
                            issues = []
                            if nulls_a > 0:
                                issues.append(f"{nulls_a:,} null(s) in Dataset A")
                            if nulls_b > 0:
                                issues.append(f"{nulls_b:,} null(s) in Dataset B")
                            if dup_a > 0:
                                issues.append(f"{dup_a:,} duplicate(s) in Dataset A")
                            if dup_b > 0:
                                issues.append(f"{dup_b:,} duplicate(s) in Dataset B")
                            st.warning(
                                f"⚠️ **Warning: `{selected_id}` is not a strict unique key ({'; '.join(issues)}).** "
                                "Matching analysis will operate on unique non-null keys, but row-level comparisons may have ambiguities."
                            )

                        # Key sets (non-null unique IDs)
                        keys_a = set(df_a[selected_id].dropna().unique())
                        keys_b = set(df_b[selected_id].dropna().unique())

                        matched_keys = keys_a.intersection(keys_b)
                        only_a_keys = keys_a - keys_b
                        only_b_keys = keys_b - keys_a

                        matched_count = len(matched_keys)
                        only_a_count = len(only_a_keys)
                        only_b_count = len(only_b_keys)

                        # Row value matching among matched IDs
                        cols_to_compare = [c for c in common_cols if c != selected_id]
                        diff_records = []
                        identical_rows_count = 0
                        diff_rows_count = 0

                        def format_val_for_display(val):
                            if pd.isna(val):
                                return "(empty / NaN)"
                            return str(val)

                        if matched_count > 0:
                            # Align subsets on matched keys without modifying source data
                            sub_a = df_a[df_a[selected_id].isin(matched_keys)].drop_duplicates(subset=[selected_id]).set_index(selected_id)
                            sub_b = df_b[df_b[selected_id].isin(matched_keys)].drop_duplicates(subset=[selected_id]).set_index(selected_id).reindex(sub_a.index)

                            if len(cols_to_compare) > 0:
                                row_has_diff = pd.Series(False, index=sub_a.index)
                                for c in cols_to_compare:
                                    eq = (sub_a[c] == sub_b[c]) | (sub_a[c].isna() & sub_b[c].isna())
                                    diff_mask = ~eq
                                    row_has_diff = row_has_diff | diff_mask
                                    diff_ids = sub_a.index[diff_mask]
                                    for id_val in diff_ids:
                                        diff_records.append({
                                            selected_id: str(id_val),
                                            "Column Name": str(c),
                                            "Value in Dataset A": format_val_for_display(sub_a.at[id_val, c]),
                                            "Value in Dataset B": format_val_for_display(sub_b.at[id_val, c])
                                        })
                                identical_rows_count = int((~row_has_diff).sum())
                                diff_rows_count = int(row_has_diff.sum())
                            else:
                                identical_rows_count = matched_count
                                diff_rows_count = 0

                        st.subheader("Matching Summary")
                        m1, m2, m3, m4, m5 = st.columns(5)
                        m1.metric("Matched IDs", f"{matched_count:,}", help="Unique keys present in both Dataset A and Dataset B")
                        m2.metric("IDs Only in Dataset A", f"{only_a_count:,}", help="Unique keys present in Dataset A but missing in Dataset B")
                        m3.metric("IDs Only in Dataset B", f"{only_b_count:,}", help="Unique keys present in Dataset B but missing in Dataset A")
                        m4.metric("Identical Matched Rows", f"{identical_rows_count:,}", help="Matched rows where all common column values are identical")
                        m5.metric("Rows with Differences", f"{diff_rows_count:,}", help="Matched rows having differences in one or more common columns")

                        st.divider()

                        # Interactive Tables
                        st.subheader(f"1. Records Only in Dataset A ({only_a_count:,} unique IDs)")
                        if only_a_count > 0:
                            st.caption("Rows from Dataset A whose key does not appear in Dataset B:")
                            df_only_a = df_a[df_a[selected_id].isin(only_a_keys)]
                            st.dataframe(df_only_a, hide_index=True)
                        else:
                            st.success("No unmatched records: All IDs in Dataset A exist in Dataset B.")

                        st.subheader(f"2. Records Only in Dataset B ({only_b_count:,} unique IDs)")
                        if only_b_count > 0:
                            st.caption("Rows from Dataset B whose key does not appear in Dataset A:")
                            df_only_b = df_b[df_b[selected_id].isin(only_b_keys)]
                            st.dataframe(df_only_b, hide_index=True)
                        else:
                            st.success("No unmatched records: All IDs in Dataset B exist in Dataset A.")

                        st.subheader(f"3. Value Differences Among Matched Records ({len(diff_records):,} field difference(s) across {diff_rows_count:,} row(s))")
                        if len(cols_to_compare) == 0:
                            st.info(f"Column `{selected_id}` is the only common column between Dataset A and Dataset B. No other common columns exist to compare.")
                        elif len(diff_records) > 0:
                            diff_df = pd.DataFrame(diff_records)
                            col_options = ["All Columns"] + sorted(list(diff_df["Column Name"].unique()))
                            chosen_filter = st.selectbox(
                                "Filter value differences by column:",
                                options=col_options,
                                key="tab2_filter_col"
                            )
                            if chosen_filter != "All Columns":
                                display_diff_df = diff_df[diff_df["Column Name"] == chosen_filter]
                            else:
                                display_diff_df = diff_df
                            st.dataframe(display_diff_df, hide_index=True)
                        elif matched_count > 0:
                            st.success("🎉 All matched rows are 100% identical across all common columns! Zero value differences found.")
                        else:
                            st.info("No matched IDs to compare values for.")

# ==============================================================================
# TAB 3: ML EXPERIMENT COMPARISON (RUN A VS RUN B)
# ==============================================================================
with tab3:
    st.header("ML Experiment Comparison")
    st.caption("Compare evaluation conditions, classification metrics, and model settings between two machine learning experiment runs.")

    # Quick fixture loader option
    t3_sample_col1, t3_sample_col2 = st.columns([2, 1])
    with t3_sample_col1:
        st.markdown("**Upload Experiment Run Files (JSON)**")
    with t3_sample_col2:
        load_samples = st.button("📁 Load M4C5 Fixtures (Run A & B)", key="tab3_load_fixtures", help="Quickly load sample files M4C5_RUN_A.json and M4C5_RUN_B.json from the course folder.")

    col_up_a, col_up_b = st.columns(2)
    with col_up_a:
        file_json_a = st.file_uploader(
            "Upload Experiment Run A (JSON)",
            type=["json"],
            key="tab3_uploader_a",
            help="Select the JSON file for Run A (e.g. baseline model)."
        )
    with col_up_b:
        file_json_b = st.file_uploader(
            "Upload Experiment Run B (JSON)",
            type=["json"],
            key="tab3_uploader_b",
            help="Select the JSON file for Run B (e.g. tuned model)."
        )

    run_a_data = None
    run_b_data = None
    source_label_a = "Uploaded File"
    source_label_b = "Uploaded File"

    # Handle sample loading button
    if "tab3_using_samples" not in st.session_state:
        st.session_state.tab3_using_samples = False

    if load_samples:
        st.session_state.tab3_using_samples = True

    # If user uploads new files, reset sample mode
    if file_json_a is not None or file_json_b is not None:
        st.session_state.tab3_using_samples = False

    if st.session_state.tab3_using_samples and file_json_a is None and file_json_b is None:
        import os
        sample_path_a = os.path.join("3-Module", "5-lesson", "M4C5_RUN_A.json")
        sample_path_b = os.path.join("3-Module", "5-lesson", "M4C5_RUN_B.json")
        try:
            with open(sample_path_a, "r", encoding="utf-8") as fa:
                run_a_data = json.load(fa)
            with open(sample_path_b, "r", encoding="utf-8") as fb:
                run_b_data = json.load(fb)
            source_label_a = "M4C5_RUN_A.json (Course Fixture)"
            source_label_b = "M4C5_RUN_B.json (Course Fixture)"
            st.info(f"Loaded fixtures: `{sample_path_a}` and `{sample_path_b}`.")
        except Exception as e:
            st.error(f"Could not load sample fixture files: {e}")

    # Process uploaded files if provided
    if file_json_a is not None:
        if file_json_a.size > MAX_FILE_SIZE_BYTES:
            st.error(f"Run A exceeds the 5 MB limit ({file_json_a.size / (1024*1024):.2f} MB).")
        elif file_json_a.size == 0:
            st.error("Uploaded Run A file is empty (0 bytes).")
        else:
            try:
                run_a_data = json.loads(file_json_a.getvalue().decode("utf-8"))
                source_label_a = file_json_a.name
            except Exception as e:
                st.error(f"Failed to parse Run A JSON: {e}")

    if file_json_b is not None:
        if file_json_b.size > MAX_FILE_SIZE_BYTES:
            st.error(f"Run B exceeds the 5 MB limit ({file_json_b.size / (1024*1024):.2f} MB).")
        elif file_json_b.size == 0:
            st.error("Uploaded Run B file is empty (0 bytes).")
        else:
            try:
                run_b_data = json.loads(file_json_b.getvalue().decode("utf-8"))
                source_label_b = file_json_b.name
            except Exception as e:
                st.error(f"Failed to parse Run B JSON: {e}")

    if run_a_data is None or run_b_data is None:
        if not st.session_state.tab3_using_samples:
            st.info("Please upload both Run A and Run B JSON files above (or click 'Load M4C5 Fixtures') to begin experiment comparison.")
    else:
        # Both JSONs available
        run_id_a = str(run_a_data.get("run_id", "Run A"))
        run_id_b = str(run_b_data.get("run_id", "Run B"))

        st.subheader(f"Experiment Comparison: `{run_id_a}` vs `{run_id_b}`")
        st.caption(f"Run A Source: {source_label_a} | Run B Source: {source_label_b}")

        st.divider()

        # ----------------------------------------------------------------------
        # 1. EVALUATION CONDITIONS CHECK
        # ----------------------------------------------------------------------
        st.subheader("1. Evaluation Conditions Consistency Check")
        st.caption("Verifying whether both experiments were tested on the exact same data split, features, target, and decision threshold.")

        eval_keys = [
            ("dataset_id", "Dataset Identifier"),
            ("split_id", "Split Identifier"),
            ("evaluation_split", "Evaluation Split (e.g. val/test)"),
            ("features", "Features Evaluated"),
            ("target", "Target Variable"),
            ("positive_class", "Positive Class Label"),
            ("threshold", "Decision Threshold"),
            ("seed", "Random Seed")
        ]

        cond_records = []
        differing_conditions = []
        missing_conditions = []

        for k, label in eval_keys:
            has_a = k in run_a_data
            has_b = k in run_b_data

            if not has_a and not has_b:
                continue

            val_a = run_a_data.get(k)
            val_b = run_b_data.get(k)

            if not has_a:
                status = "❌ Missing in Run A"
                missing_conditions.append(f"{label} (`{k}`) is missing in Run A")
            elif not has_b:
                status = "❌ Missing in Run B"
                missing_conditions.append(f"{label} (`{k}`) is missing in Run B")
            else:
                if isinstance(val_a, list) and isinstance(val_b, list):
                    eq = (sorted(str(x) for x in val_a) == sorted(str(x) for x in val_b))
                else:
                    eq = (val_a == val_b)

                if eq:
                    status = "✅ Match"
                else:
                    status = "⚠️ Different"
                    differing_conditions.append(f"{label} (`{k}`): Run A has `{val_a}`, Run B has `{val_b}`")

            # Formatting for display
            display_a = ", ".join(str(x) for x in val_a) if isinstance(val_a, list) else str(val_a) if has_a else "(Not Recorded)"
            display_b = ", ".join(str(x) for x in val_b) if isinstance(val_b, list) else str(val_b) if has_b else "(Not Recorded)"

            cond_records.append({
                "Evaluation Condition": label,
                f"Run A ({run_id_a})": display_a,
                f"Run B ({run_id_b})": display_b,
                "Status": status
            })

        cond_df = pd.DataFrame(cond_records)
        st.dataframe(cond_df, hide_index=True)

        # Clear banner report
        if not differing_conditions and not missing_conditions:
            st.success(
                "✅ **Evaluation Conditions Match**: All recorded evaluation conditions are identical across both runs. "
                "The metric differences represent a controlled, valid comparison."
            )
        else:
            warning_lines = []
            if missing_conditions:
                warning_lines.append("**Missing Conditions:**\n" + "\n".join(f"- {c}" for c in missing_conditions))
            if differing_conditions:
                warning_lines.append("**Different Conditions:**\n" + "\n".join(f"- {c}" for c in differing_conditions))

            st.warning(
                "⚠️ **Evaluation Conditions Mismatch / Missing Detected**:\n\n"
                + "\n\n".join(warning_lines)
                + "\n\n*Note: When evaluation conditions differ, metric differences may reflect split/data/threshold discrepancies rather than true model performance changes.*"
            )

        st.divider()

        # ----------------------------------------------------------------------
        # 2. CORE CLASSIFICATION METRICS (F1, PRECISION, RECALL) & DIFFERENCES
        # ----------------------------------------------------------------------
        st.subheader("2. Metrics Comparison: F1-score, Precision & Recall")
        st.caption("Differences are computed strictly as (Run B − Run A). Positive delta indicates higher score in Run B.")

        metrics_a = run_a_data.get("metrics", {}) if isinstance(run_a_data.get("metrics"), dict) else {}
        metrics_b = run_b_data.get("metrics", {}) if isinstance(run_b_data.get("metrics"), dict) else {}

        target_metrics = [
            ("f1", "F1-Score"),
            ("precision", "Precision"),
            ("recall", "Recall"),
            ("train_f1", "Train F1-Score (Overfitting Check)")
        ]

        m_cols = st.columns(len(target_metrics))
        metrics_table_rows = []

        for idx, (m_key, m_name) in enumerate(target_metrics):
            val_a = metrics_a.get(m_key)
            val_b = metrics_b.get(m_key)

            if val_a is not None and val_b is not None:
                try:
                    num_a = float(val_a)
                    num_b = float(val_b)
                    diff = num_b - num_a
                    diff_str = f"{diff:+.4f}"
                    val_a_str = f"{num_a:.4f}"
                    val_b_str = f"{num_b:.4f}"
                    pct_change = f"{(diff / num_a * 100):+.2f}%" if num_a != 0 else "N/A"
                except Exception:
                    diff_str = "N/A"
                    val_a_str = str(val_a)
                    val_b_str = str(val_b)
                    pct_change = "N/A"
            else:
                val_a_str = str(val_a) if val_a is not None else "(Missing)"
                val_b_str = str(val_b) if val_b is not None else "(Missing)"
                diff_str = "N/A"
                pct_change = "N/A"

            # Display metric card
            with m_cols[idx]:
                if diff_str != "N/A":
                    st.metric(
                        label=m_name,
                        value=val_b_str,
                        delta=f"{diff_str} (vs A: {val_a_str})",
                        help=f"Run B: {val_b_str} | Run A: {val_a_str} | Difference (B − A): {diff_str}"
                    )
                else:
                    st.metric(label=m_name, value=val_b_str, delta=None)

            metrics_table_rows.append({
                "Metric": m_name,
                f"Run A ({run_id_a})": val_a_str,
                f"Run B ({run_id_b})": val_b_str,
                "Difference (B − A)": diff_str,
                "Relative Change (%)": pct_change
            })

        st.dataframe(pd.DataFrame(metrics_table_rows), hide_index=True)

        st.info(
            "ℹ️ **Objective Evaluation Notice**: No automated winner is declared. "
            "Model selection depends on whether your problem prioritizes higher precision (avoiding false alarms) "
            "or higher recall (catching all positive cases), as well as model complexity and deployment latency."
        )

        st.divider()

        # ----------------------------------------------------------------------
        # 3. MODEL SETTINGS & HYPERPARAMETERS
        # ----------------------------------------------------------------------
        st.subheader("3. Model Settings & Hyperparameters")
        st.caption("Model configurations and hyperparameters recorded in each run:")

        excluded_keys = set([k for k, _ in eval_keys]).union({
            "format_version", "run_id", "metrics", "note"
        })

        all_keys = sorted(list(set(run_a_data.keys()).union(set(run_b_data.keys()))))
        model_setting_keys = [k for k in all_keys if k not in excluded_keys]

        if not model_setting_keys:
            st.write("No distinct model settings found in the uploaded JSON files.")
        else:
            settings_rows = []
            for k in model_setting_keys:
                has_a = k in run_a_data
                has_b = k in run_b_data
                sa = run_a_data.get(k)
                sb = run_b_data.get(k)

                if has_a and has_b:
                    status = "✅ Identical" if sa == sb else "🔄 Different"
                elif has_a:
                    status = "Present only in Run A"
                else:
                    status = "Present only in Run B"

                settings_rows.append({
                    "Setting / Hyperparameter": k,
                    f"Run A ({run_id_a})": str(sa) if has_a else "(Not Set)",
                    f"Run B ({run_id_b})": str(sb) if has_b else "(Not Set)",
                    "Status": status
                })

            st.dataframe(pd.DataFrame(settings_rows), hide_index=True)

        # Show experiment notes if present
        note_a = run_a_data.get("note")
        note_b = run_b_data.get("note")
        if note_a or note_b:
            with st.expander("📝 Experiment Notes & Metadata", expanded=False):
                if note_a:
                    st.markdown(f"**Run A Note:** {note_a}")
                if note_b:
                    st.markdown(f"**Run B Note:** {note_b}")
