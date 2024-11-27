from pathlib import Path

# PROJECT_DIR = Path(__file__).resolve().resolve().parents[2]
PROJECT_DIR = Path("/home/hongyi/Docs2KG_Proto")

DATA_DIR = PROJECT_DIR / "data"
DOC_DIR = PROJECT_DIR / "docs"

DATA_INPUT_DIR = DATA_DIR / "input"
"""
This is Output directory for the data

Example
```
from Docs2KG.utils.constants import DATA_OUTPUT_DIR
```
"""

DATA_OUTPUT_DIR = DATA_DIR / "output"
# if not exists, create the directories


DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_INPUT_DIR.mkdir(parents=True, exist_ok=True)
