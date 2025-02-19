# Panerai Watch Market Analysis

## Overview
Analysis tool for Panerai watches, featuring price arbitrage detection, trend analysis, and price predictions. Built with secure data handling and clean environment management.

## Key Features
- **Data Loading**: Secure BigQuery integration for watch price data
- **Data Processing**: Robust cleaning and standardization pipeline
- **Market Analysis**: 
  - Arbitrage opportunity detection across currencies
  - Price trend analysis and forecasting
  - Collection-based analytics
- **Interactive Visualization**: Streamlit dashboard for real-time analysis
- **Secure Environment**: Managed with pyenv and direnv for reproducibility

## Prerequisites
- Python 3.12.1
- WSL2 (for Windows users)
- Git
- VS Code with Python and WSL extensions
- BigQuery credentials
- pyenv
- direnv

## Quick Setup
1. **Clone and Setup Environment**
```bash
git clone https://github.com/Clemtourte/group4_BD_mgt.git
cd group4_BD_mgt
pyenv install 3.12.1
pyenv local 3.12.1
direnv allow
```

2. **Configure Credentials**
- Place your BigQuery credentials file in the project root
- Set up `.env`:
```
GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

3. **Install Dependencies**
```bash
make install
```

## Usage
### Core Commands
```bash
make all          # Run install, clean, and main pipeline
make run          # Run main analysis pipeline
make clean        # Clean temporary files and caches
make install      # Install package and dependencies
make streamlit    # Launch visualization dashboard
```

### Project Structure
```
group4_BD_mgt/
├── bdm_analysis/           
│   ├── notebooks/         # Jupyter notebooks for testing
│   ├── streamlit/         # Streamlit-based visualization components
│       ├──app.py             # Streamlit web app entry point
│   ├── clean_data.py      # Data cleaning functions (currency conversion, missing data handling)
│   ├── load_data.py       # Queries BigQuery and loads watch data
│   ├── predicting_algo.py # Linear regression model for price forecasting
│   ├── arbitrage_analysis.py # Arbitrage detection logic
│   ├── analyze_data.py    # Various analysis functions (collections, trends, price ranges)
│   ├── main.py            # End-to-end execution pipeline
├── Makefile           # Automation commands for installation and execution
├── requirements.txt   # Required Python dependencies
├── setup.py           # Package installation setup
└── .envrc             # Environment variable configurations
```

## Key Files
- `clean_data.py`: Data cleaning and standardization
- `load_data.py`: Secure BigQuery data retrieval
- `arbitrage_analysis.py`: Cross-currency arbitrage detection
- `predicting_algo.py`: Price prediction algorithms
- `main.py`: Pipeline orchestration
- `.envrc`: Environment configuration with direnv
- `Makefile`: Build and execution automation

## Environment Configuration
### Environment Variables (.envrc)
```bash
export MODEL_TARGET="local"
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/group4_BD_mgt/credentials.json"
export PYTHONPATH="$PWD:$PYTHONPATH"
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
```

### Environment Management
The project uses:
- **pyenv**: Python version management
- **direnv**: Automatic environment loading

## Development Workflow
1. Create feature branch from main
2. Make your changes
3. Run full pipeline: `make all`
4. Commit and push changes
5. Create pull request

## Dashboard
The Streamlit dashboard provides:
- Arbitrage opportunity detection
- Price prediction visualization
- Interactive market analysis tools

Launch with:
```bash
make streamlit
```

## Common Issues
- WSL2 not installed: Follow WSL installation guide
- direnv not loading: Run `direnv allow`
- Import errors: Verify `make install` was run
- BigQuery errors: Check credentials path in `.env`
- Package errors: Run `make requirements` to update dependencies

## Makefile Commands
- `make requirements`: Update requirements.txt file
- `make install`: Install or update project dependencies
- `make clean`: Remove temporary files and caches
- `make run`: Execute main analysis pipeline
- `make streamlit`: Launch the visualization dashboard
- `make all`: Full pipeline (install, clean, run)

## Security
- Secure credential management via environment variables
- BigQuery authentication through service account
- Isolated Python environment for dependency control
