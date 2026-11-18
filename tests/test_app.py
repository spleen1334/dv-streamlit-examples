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
