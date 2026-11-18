from datetime import date
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

from sales_data import load_sales


APP = Path(__file__).resolve().parents[1] / "streamlit_app.py"


class SalesLabTests(unittest.TestCase):
    def test_basics_filters_sales_on_rerun(self):
        sales = load_sales()
        app = AppTest.from_file(str(APP)).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.title[0].value, "Chart basics")
        self.assertEqual(len(app.dataframe[0].value), len(sales))

        app.selectbox(key="basics_region").select("North").run()

        self.assertFalse(app.exception)
        self.assertEqual(set(app.dataframe[0].value["region"]), {"North"})
        self.assertEqual(len(app.dataframe[0].value), int(sales["region"].eq("North").sum()))

    def test_analysis_applies_filters_only_on_submit(self):
        app = AppTest.from_file(str(APP)).run()
        app.switch_page("app_pages/interactive_analysis.py").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.dataframe[0].value), 18)

        app.multiselect(key="analysis_products").set_value(["Desk Lamp"]).run()
        self.assertEqual(len(app.dataframe[0].value), 18)

        # AppTest submits widget state on each run rather than buffering form edits in a browser.
        app.multiselect(key="analysis_products").set_value(["Desk Lamp"])
        app.date_input(key="analysis_dates").set_value(
            (date(2025, 1, 8), date(2025, 3, 31))
        )
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.dataframe[0].value["Product"].tolist(), ["Desk Lamp"] * 3)
        self.assertEqual(app.dataframe[0].value["Revenue (USD)"].tolist(), [1400, 1470, 1505])

        app.multiselect(key="analysis_products").set_value([])
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertIn("No products selected", app.info[0].value)
        self.assertEqual(len(app.dataframe), 0)
