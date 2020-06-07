import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
admin_id = os.getenv("ADMIN_ID")
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
main_page = os.getenv("MAIN_PAGE")
marathon_duration = int(os.getenv("MARATHON_DURATION"))

START_DATE = datetime.strptime(os.getenv("START_DATE"), '%Y-%m-%d')
DB_NAME = "daily_ration.db"
