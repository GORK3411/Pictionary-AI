from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = 42
CATEGORIES_PATH = ROOT/"categories"
DATA_PATH = ROOT/"data"
PROCESSED_DATA_PATH = DATA_PATH/"processed"
RAW_DATA_PATH = DATA_PATH/"raw"
CLEANED_PATH = PROCESSED_DATA_PATH/"cleaned.ndjson"
SPLIT_PATH = PROCESSED_DATA_PATH/"split.json"