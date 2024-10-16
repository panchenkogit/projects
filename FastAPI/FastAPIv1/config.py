import os
from dotenv import load_dotenv


load_dotenv()

SQL_DB_URL = os.environ.get("SQL_DB_URL")

