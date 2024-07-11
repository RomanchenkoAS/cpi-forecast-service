import os


ROSSTAT_BASE_URL = "https://rosstat.gov.ru/"
ROSSTAT_CPI_DATA_URL = "https://rosstat.gov.ru/storage/mediabank/Nedel_ipc.xlsx"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")  # Directory with temporary data
DATA_FILE_PATH = os.path.join(DATA_DIR, "price_data_long.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models/trained_models")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
