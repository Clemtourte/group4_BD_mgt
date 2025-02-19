requirements:
	@pip freeze | grep -v "bdm_analysis" > requirements_new.txt
	@if ! cmp -s requirements.txt requirements_new.txt; then mv requirements_new.txt requirements.txt; echo "✅ requirements.txt updated"; else rm requirements_new.txt; echo "🔄 requirements.txt is already up to date"; fi

install: requirements
	@if [ requirements.txt -nt .installed ]; then pip install -e . && touch .installed; fi

clean:
	@rm -f version.txt
	@rm -f .coverage
	@rm -rf .ipynb_checkpoints
	@rm -rf build
	@rm -rf __pycache__
	@find . -name "*.pyc" -delete

run: install
	@python -m bdm_analysis.main

all: install clean run
