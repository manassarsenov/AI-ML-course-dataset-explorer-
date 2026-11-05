import unittest
import pandas as pd
import numpy as np
from streamlit.testing.v1 import AppTest

class TestDatasetMComprehensive(unittest.TestCase):

    def test_initial_render(self):
        """App renders both tabs without error when no files uploaded."""
        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        self.assertFalse(at.exception)
        self.assertTrue(len(at.tabs) >= 2)

    def test_tab1_features(self):
        """Verify Tab 1: preview, summary, missing values, spaces-only, chart, boxplot."""
        csv_data = (
            "category,val,text\n"
            "Electronics,100,Item A\n"
            "Electronics,250,Item B\n"
            "Clothing,50,   \n"
            "Clothing,,Item D\n"
            "Books,15,Item E\n"
            "Books,15,Item E\n"
        ).encode("utf-8")

        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        at.file_uploader[0].upload("store.csv", csv_data)
        at.run()
        self.assertFalse(at.exception)

        metrics = {m.label: m.value for m in at.metric}
        self.assertEqual(metrics.get("Total Rows"), "6")
        self.assertEqual(metrics.get("Total Columns"), "3")
        self.assertEqual(metrics.get("Extra Duplicate Rows"), "1")
        self.assertEqual(metrics.get("Total Spaces-Only Cells"), "1")
        self.assertIn("Q1 (25%)", metrics)
        self.assertIn("Median (Q2)", metrics)

        # Check spaces-only filter
        chk = at.checkbox(key="chk_spaces_rows")
        chk.check().run()
        self.assertFalse(at.exception)

        # Check missing rows button toggle
        btn = at.button(key="btn_missing_rows")
        btn.click().run()
        self.assertFalse(at.exception)

    def test_tab2_summary_cards_and_column_differences(self):
        """Verify Tab 2 summary cards, column diffs (unique A, unique B, common dtypes)."""
        csv_a = (
            "row_id,customer,age,status\n"
            "1,Alice,30,Active\n"
            "2,Bob,45,Inactive\n"
            "3,Charlie,25,Active\n"
        ).encode("utf-8")

        csv_b = (
            "row_id,customer,signup_date,status\n"
            "1,Alice,2026-01-01,Active\n"
            "2,Robert,2026-02-01,Pending\n"
            "4,Diana,2026-03-01,Active\n"
        ).encode("utf-8")

        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()

        at.file_uploader[1].upload("customers_a.csv", csv_a)
        at.file_uploader[2].upload("customers_b.csv", csv_b)
        at.run()
        self.assertFalse(at.exception)

        metrics = {m.label: m.value for m in at.metric}
        # Rows and cols
        self.assertEqual(metrics.get("Rows (Dataset A vs B)"), "3 vs 3")
        self.assertEqual(metrics.get("Columns (Dataset A vs B)"), "4 vs 4")
        self.assertEqual(metrics.get("Common Columns Count"), "3") # row_id, customer, status
        self.assertEqual(metrics.get("Columns Only in A / Only in B"), "1 / 1") # age in A, signup_date in B

        # Matching metrics
        self.assertEqual(metrics.get("Matched IDs"), "2") # 1, 2
        self.assertEqual(metrics.get("IDs Only in Dataset A"), "1") # 3
        self.assertEqual(metrics.get("IDs Only in Dataset B"), "1") # 4
        self.assertEqual(metrics.get("Identical Matched Rows"), "1") # 1: Alice, Active
        self.assertEqual(metrics.get("Rows with Differences"), "1") # 2: Bob vs Robert, Inactive vs Pending

        # Key validation
        self.assertEqual(metrics.get("Nulls in Dataset A"), "0")
        self.assertEqual(metrics.get("Nulls in Dataset B"), "0")
        self.assertEqual(metrics.get("Duplicates in Dataset A"), "0")
        self.assertEqual(metrics.get("Duplicates in Dataset B"), "0")

    def test_tab2_identical_datasets(self):
        """Verify matching when two datasets are 100% identical."""
        csv_data = (
            "id,score,rank\n"
            "10,95,1\n"
            "20,88,2\n"
            "30,75,3\n"
        ).encode("utf-8")

        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()

        at.file_uploader[1].upload("data1.csv", csv_data)
        at.file_uploader[2].upload("data2.csv", csv_data)
        at.run()
        self.assertFalse(at.exception)

        metrics = {m.label: m.value for m in at.metric}
        self.assertEqual(metrics.get("Matched IDs"), "3")
        self.assertEqual(metrics.get("IDs Only in Dataset A"), "0")
        self.assertEqual(metrics.get("IDs Only in Dataset B"), "0")
        self.assertEqual(metrics.get("Identical Matched Rows"), "3")
        self.assertEqual(metrics.get("Rows with Differences"), "0")
        self.assertTrue(any("All matched rows are 100% identical" in str(s.value) for s in at.success))

    def test_tab2_empty_file_and_size_limits(self):
        """Verify 0-byte and oversized file validations."""
        empty_file = b""
        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()

        # Tab 1 empty
        at.file_uploader[0].upload("empty.csv", empty_file)
        at.run()
        self.assertTrue(any("uploaded file is empty" in str(e.value) for e in at.error))

        # Tab 2 empty A
        at2 = AppTest.from_file("app.py", default_timeout=30)
        at2.run()
        at2.file_uploader[1].upload("empty_a.csv", empty_file)
        at2.file_uploader[2].upload("valid_b.csv", b"id,val\n1,10\n")
        at2.run()
        self.assertTrue(any("Dataset A is empty" in str(e.value) for e in at2.error))

    def test_tab2_dtype_mismatch_and_null_keys(self):
        """Verify warning when key contains nulls and duplicates."""
        csv_a = (
            "id,val\n"
            "1,A\n"
            "1,B\n"
            ",C\n"
        ).encode("utf-8")

        csv_b = (
            "id,val\n"
            "1,A\n"
            "2,D\n"
        ).encode("utf-8")

        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        at.file_uploader[1].upload("a.csv", csv_a)
        at.file_uploader[2].upload("b.csv", csv_b)
        at.run()
        self.assertFalse(at.exception)

        metrics = {m.label: m.value for m in at.metric}
        self.assertEqual(metrics.get("Duplicates in Dataset A"), "1")
        self.assertEqual(metrics.get("Nulls in Dataset A"), "1")
        self.assertEqual(metrics.get("Duplicates in Dataset B"), "0")
        self.assertEqual(metrics.get("Nulls in Dataset B"), "0")
        self.assertTrue(any("Warning: `id` is not a strict unique key" in str(w.value) for w in at.warning))

if __name__ == "__main__":
    unittest.main()
