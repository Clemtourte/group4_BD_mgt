install:
	@pip install -e .

clean:
	@rm -f version.txt
	@rm -f .coverage
	@rm -rf .ipynb_checkpoints
	@rm -rf build
	@rm -rf __pycache__
	@find . -name "*.pyc" -delete

load_data:
	@python -c "from bdm_analysis.load_data import load_data_from_bigquery; load_data_from_bigquery()"

clean_data:
	@python -c "from bdm_analysis.load_data import load_data_from_bigquery; from bdm_analysis.clean_data import clean_data; df = load_data_from_bigquery(); df = clean_data(df)"

run:
	@python -m bdm_analysis.main

all: install clean