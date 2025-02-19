requirements:
	@pip freeze | grep -v "bdm_analysis" > requirements.txt

install: requirements
	@pip install -e .

clean:
	@rm -f version.txt
	@rm -f .coverage
	@rm -rf .ipynb_checkpoints
	@rm -rf build
	@rm -rf __pycache__
	@find . -name "*.pyc" -delete

run: requirements
	@python -m bdm_analysis.main

all: install clean run
