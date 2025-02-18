install:
	@pip install -e .

clean:
	@if exist version.txt del /F /Q version.txt
	@if exist .coverage del /F /Q .coverage
	@if exist .ipynb_checkpoints rmdir /S /Q .ipynb_checkpoints
	@if exist build rmdir /S /Q build
	@if exist __pycache__ rmdir /S /Q __pycache__
	@del /F /Q *.pyc 2>nul || exit 0

all: install clean