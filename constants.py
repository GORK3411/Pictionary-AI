from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = 42
CATEGORIES_PATH = ROOT/"categories"
DATA_PATH = ROOT/"data"
PROCESSED_DATA_PATH = DATA_PATH/"processed"
RAW_DATA_PATH = DATA_PATH/"raw"