.DEFAULT_GOAL := help
.PHONY: help setup run test

help:
	@printf '%s\n' 'make setup  Install locked dependencies' 'make run    Launch the Streamlit app' 'make test   Run the unittest suite'

setup:
	uv sync --locked

run:
	uv run --locked streamlit run streamlit_app.py

test:
	uv run --locked python -m unittest discover -s tests -v
