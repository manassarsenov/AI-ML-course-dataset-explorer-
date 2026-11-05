import pandas as pd
import numpy as np

def test_chart_calculation():
    # Synthetic test matching the user's test specification: A totals 30 and B totals 10
    test_data = {
        "Category": ["A", "A", "B", "C", "C", None, "D"],
        "Value": [10, 20, 10, np.nan, np.nan, 99, 5]
    }
    df = pd.DataFrame(test_data)
    
    selected_category = "Category"
    selected_numeric = "Value"
    
    # Check missing category
    missing_cat_mask = df[selected_category].isna()
    missing_cat_count = int(missing_cat_mask.sum())
    assert missing_cat_count == 1, f"Expected 1 missing category row, got {missing_cat_count}"
    
    # Filter valid
    valid_cat_df = df[~missing_cat_mask]
    
    # Group sum with min_count=1
    category_sums = valid_cat_df.groupby(selected_category)[selected_numeric].agg(lambda s: s.sum(min_count=1))
    sorted_totals = category_sums.sort_values(ascending=False, na_position="last")
    
    # Verify A = 30 and B = 10
    total_A = sorted_totals.get("A")
    total_B = sorted_totals.get("B")
    total_C = sorted_totals.get("C")
    
    assert total_A == 30, f"Expected A to total 30, got {total_A}"
    assert total_B == 10, f"Expected B to total 10, got {total_B}"
    assert pd.isna(total_C), f"Expected C (all NaN) to be NaN, got {total_C}"
    
    # Helper formatting
    def format_display_total(val):
        if pd.isna(val):
            return "No data"
        if isinstance(val, (int, np.integer)) or (isinstance(val, (float, np.floating)) and float(val).is_integer()):
            return f"{int(val):,}"
        return f"{val:,.4f}".rstrip("0").rstrip(".")
    
    assert format_display_total(total_A) == "30"
    assert format_display_total(total_B) == "10"
    assert format_display_total(total_C) == "No data"
    
    print("ALL_ASSERTIONS_PASSED: A=30, B=10, C='No data', MissingCategoryCount=1")

if __name__ == "__main__":
    test_chart_calculation()
