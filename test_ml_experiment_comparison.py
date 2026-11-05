import unittest
import json
import os
from streamlit.testing.v1 import AppTest

class TestMLExperimentComparison(unittest.TestCase):

    def setUp(self):
        self.path_a = os.path.join("3-Module", "5-lesson", "M4C5_RUN_A.json")
        self.path_b = os.path.join("3-Module", "5-lesson", "M4C5_RUN_B.json")
        with open(self.path_a, "r", encoding="utf-8") as f:
            self.json_bytes_a = f.read().encode("utf-8")
        with open(self.path_b, "r", encoding="utf-8") as f:
            self.json_bytes_b = f.read().encode("utf-8")

    def test_tab3_m4c5_fixtures_upload(self):
        """Test uploading M4C5_RUN_A.json and M4C5_RUN_B.json into Tab 3."""
        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        self.assertFalse(at.exception)

        # Upload to Tab 3's uploaders (index 3 and 4 in file_uploader list)
        # file_uploader[0]: Tab 1
        # file_uploader[1]: Tab 2 A
        # file_uploader[2]: Tab 2 B
        # file_uploader[3]: Tab 3 A
        # file_uploader[4]: Tab 3 B
        at.file_uploader[3].upload("M4C5_RUN_A.json", self.json_bytes_a)
        at.file_uploader[4].upload("M4C5_RUN_B.json", self.json_bytes_b)
        at.run()
        self.assertFalse(at.exception)

        # Check metrics
        metrics = {m.label: (m.value, m.delta) for m in at.metric}
        self.assertIn("F1-Score", metrics)
        self.assertIn("Precision", metrics)
        self.assertIn("Recall", metrics)

        # Check F1
        f1_val, f1_delta = metrics["F1-Score"]
        self.assertEqual(f1_val, "0.6300")
        self.assertIn("+0.0300", f1_delta)

        # Check Precision
        prec_val, prec_delta = metrics["Precision"]
        self.assertEqual(prec_val, "0.6700")
        self.assertIn("+0.0300", prec_delta)

        # Check Recall
        rec_val, rec_delta = metrics["Recall"]
        self.assertEqual(rec_val, "0.5900")
        self.assertIn("+0.0200", rec_delta)

        # Check condition success alert
        successes = [s.value for s in at.success]
        self.assertTrue(any("Evaluation Conditions Match" in s for s in successes))

        # Check model settings table is rendered
        # Ensure 'C' difference is reflected
        dfs = [df.value for df in at.dataframe]
        self.assertTrue(len(dfs) >= 2)

        # Ensure no automatic winner is chosen (info message present)
        infos = [i.value for i in at.info]
        self.assertTrue(any("No automated winner is declared" in i for i in infos))

    def test_tab3_condition_mismatch_and_missing(self):
        """Test that different or missing evaluation conditions are clearly reported."""
        run_a = json.loads(self.json_bytes_a.decode("utf-8"))
        run_b = json.loads(self.json_bytes_b.decode("utf-8"))

        # Modify run_b to have a different evaluation threshold and missing split_id
        run_b["threshold"] = 0.65
        del run_b["split_id"]

        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        at.file_uploader[3].upload("RunA.json", json.dumps(run_a).encode("utf-8"))
        at.file_uploader[4].upload("RunB_mod.json", json.dumps(run_b).encode("utf-8"))
        at.run()
        self.assertFalse(at.exception)

        # Verify warning about mismatch/missing
        warnings = [w.value for w in at.warning]
        self.assertTrue(any("Evaluation Conditions Mismatch / Missing Detected" in w for w in warnings))

    def test_existing_tabs_continue_working(self):
        """Verify Tab 1 and Tab 2 still function without regression."""
        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.tabs), 3)

if __name__ == "__main__":
    unittest.main()
