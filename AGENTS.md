# AGENTS.md

Guidelines for AI coding agents working in this repository.

## Project Overview

Gallaflow is a forecasting application for predicting discharge (water flow) on the Gallatin River in Montana. It combines SNOTEL snow data with USGS water data to build machine learning models (XGBoost, Prophet) for river flow prediction.

## Build/Lint/Test Commands

### Environment Setup

```bash
cd explore
uv sync                    # Install dependencies
uv run python hello.py     # Verify installation
```

### Running Python Scripts

```bash
cd explore
uv run python <script.py>  # Run a specific script
```

### Jupyter Notebooks

```bash
cd explore
uv run jupyter lab         # Start Jupyter Lab server
```

### Linting/Type Checking

No linter or type checker is currently configured. If adding one, prefer:
- **ruff** for linting and formatting
- **pyright** or **mypy** for type checking

```bash
# Recommended commands to add:
uv add --dev ruff pyright
uv run ruff check .
uv run ruff format .
uv run pyright
```

### Testing

No tests currently exist. When adding tests, use pytest:

```bash
uv add --dev pytest
uv run pytest                    # Run all tests
uv run pytest tests/test_x.py    # Run single test file
uv run pytest tests/test_x.py::test_name  # Run single test
```

## Code Style Guidelines

### Imports

```python
# Standard library first
import json
import os
import re
from datetime import datetime

# Third-party libraries second
import numpy as np
import pandas as pd
import requests
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# Local imports last (if any)
```

- Group imports: standard library, third-party, local
- Use absolute imports for local modules
- Alphabetize within each group when practical

### Formatting

- Use 4 spaces for indentation (no tabs)
- Max line length: ~100 characters
- Break long function calls with aligned arguments:

```python
response = requests.get(
    base_url,
    params={
        'sites': '06043500',
        'startDT': start_date,
        'endDT': end_date,
    }
)
```

- Trailing commas in multi-line structures

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `daily_cfs`, `start_date` |
| Functions | snake_case | `load_cfs()`, `create_date_features()` |
| Constants | UPPER_SNAKE | `TARGET`, `FEATURES` |
| DataFrames | descriptive snake_case | `merged_df`, `hourly_cfs` |
| File names | snake_case | `get_cfs_daily.py`, `merge_hourly.py` |

### Types

- Python 3.12+ is required
- Type hints are encouraged but not strictly enforced
- For new modules, add type hints to function signatures:

```python
def load_cfs(path: str) -> pd.DataFrame:
    ...

def create_date_features(df: pd.DataFrame) -> pd.DataFrame:
    ...
```

### Error Handling

Current code uses simple print statements for errors:

```python
if response.status_code != 200:
    print('You fucked up something. Code: ', response.status_code)
```

For production code, prefer proper exception handling:

```python
if response.status_code != 200:
    raise RuntimeError(f"API request failed: {response.status_code}")
```

- Use specific exception types
- Include relevant context in error messages
- Log errors appropriately for production

### Data Pipeline Patterns

The project follows a consistent pattern:

1. **Data fetching** (`get_*.py`): Download raw data from APIs
   - USGS water data: `get_cfs_daily.py`, `get_cfs_hourly.py`
   - SNOTEL snow data: `get_sntl_daily.py`, `get_sntl_hourly.py`
   - Save to `data/raw/`

2. **Data merging** (`merge_*.py`): Combine and clean datasets
   - Parse JSON/CSV responses
   - Merge on date index
   - Save to `data/`

3. **Modeling** (`xgb_*.py`, notebooks): Train and evaluate models

### DataFrame Conventions

- Use `date` as the index column for time series
- Parse dates explicitly: `pd.read_csv(..., parse_dates=['date'])`
- Use `inplace=True` sparingly; prefer `df = df.copy()` then return new df
- Feature engineering functions should accept and return DataFrames

### Jupyter Notebooks

Notebooks are used for exploration and visualization:
- `explore.ipynb`, `explore_daily.ipynb`: Initial data exploration
- `xgb_daily.ipynb`, `xgb_daily2.ipynb`: XGBoost model development
- `prophet_daily.ipynb`: Prophet model development
- `hybrid.ipynb`: Combined model approaches

Keep production code in `.py` files; notebooks for experimentation.

### Constants and Configuration

Key data source identifiers:

```python
USGS_STATION = '06043500'  # Gallatin Gateway station
SNOTEL_STATION = '754:MT:SNTL'  # Shower Falls location
```

API endpoints:
- USGS daily: `https://nwis.waterdata.usgs.gov/nwis/dv`
- USGS hourly: `https://waterservices.usgs.gov/nwis/iv/`
- SNOTEL: `https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data`

## Project Structure

```
gallaflow/
├── README.md           # Project overview
├── .gitignore
└── explore/            # Main code directory
    ├── pyproject.toml  # Dependencies (uv)
    ├── uv.lock         # Lock file
    ├── .python-version # Python 3.12
    ├── data/           # Processed data
    │   └── raw/        # Raw API responses
    ├── get_*.py        # Data fetching scripts
    ├── merge_*.py      # Data merging scripts
    ├── xgb_*.py        # XGBoost model scripts
    └── *.ipynb         # Jupyter notebooks
```

## Dependencies

Core packages (defined in `explore/pyproject.toml`):
- pandas, numpy: Data manipulation
- scikit-learn: ML utilities and metrics
- xgboost: Gradient boosting models
- prophet: Time series forecasting
- seaborn, matplotlib: Visualization
- ipykernel: Jupyter support

Use `uv add <package>` to add new dependencies.
