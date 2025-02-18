install:
	@pip install -e .

clean:
	@rm -f version.txt
	@rm -f .coverage
	@rm -rf .ipynb_checkpoints
	@rm -rf build
	@rm -rf __pycache__
	@find . -name "*.pyc" -delete

all: install clean
