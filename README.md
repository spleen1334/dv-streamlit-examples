# Streamlit Sales Lab

Learn how to turn a pandas DataFrame into an interactive dashboard. Three small lessons use the same fictional sales data, so you can focus on what changes in the code from page to page.

## What Streamlit is good for

[Streamlit](https://docs.streamlit.io/get-started/fundamentals/main-concepts) is an open-source Python framework for building interactive data apps. It’s useful for KPI dashboards, exploratory analysis, internal tools, and machine-learning demos. You can pass a DataFrame directly to a table or chart and add widgets without having to build a separate JavaScript frontend.

The trade-off is that the built-in layout and widgets offer less control than a custom frontend. Streamlit also normally reruns the script from top to bottom when a widget changes. That makes it easy to connect an input to a chart, but expensive computations may need caching and values that must survive a rerun may need Session State.

**Cost:** The [library is free under Apache 2.0](https://github.com/streamlit/streamlit#license). This project runs locally without an account. [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud) offers free hosting with [resource limits](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/understand-app-resources). Self-hosting or using a commercial platform can mean paying for compute and operations.

| Alternative | When to try it |
| --- | --- |
| [Plotly Dash](https://dash.plotly.com/basic-callbacks) | You want to explicitly wire component inputs to outputs using callbacks. |
| [Shiny for Python](https://shiny.posit.co/py/docs/overview.html) | You want a reactive engine that tracks dependencies between inputs and calculations. |
| [HoloViz Panel](https://panel.holoviz.org/) | You work in notebooks or want to mix components from multiple Python visualization libraries. |

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and have `make` available. From the project directory:

```sh
make setup
make run
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`). Press `Ctrl+C` to stop. `make setup` installs the locked dependencies for Python 3.13 into `.venv`; no manual activation is needed. Run `make test` for the automated checks or `make help` for the available commands.

## Learning path

1. **Chart Basics** — Change the region and see the table and built-in charts update immediately. In `app_pages/chart_basics.py`, find the filter and follow the data through the pandas aggregations to the charts. **Try:** change the bar chart from revenue to quantity and update its label.
2. **Interactive Analysis** — Change the product and date filters, then click **Apply filters**. In `app_pages/interactive_analysis.py`, follow the applied filters into the Altair chart and hover over a mark to see its tooltip. **Try:** add a different field to the tooltip. The contrast with the first page shows what [forms](https://docs.streamlit.io/develop/concepts/architecture/forms) do: the browser sends the form’s widget values together on submission.
3. **Component Playground** — Try layout, input, editing, feedback, and download components without needing to understand the full dashboard. **Try:** edit a quantity and watch the total change, then reload to see that the original data is still intact. The [API reference](https://docs.streamlit.io/develop/api-reference) lists more components to explore.

Start reading at `streamlit_app.py`: it registers each page using `st.Page`, passes the pages to `st.navigation`, and runs the selected page, like the [official multipage tutorial](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app). The page scripts are in `app_pages/`, `sales_data.py` loads the bundled `data/sales.csv`, and `tests/test_app.py` exercises the running scripts using Streamlit’s [AppTest](https://docs.streamlit.io/develop/concepts/app-testing).
