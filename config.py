from dotenv import load_dotenv
import os
load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
DRIVER_NAME = os.getenv('DRIVER_NAME')
DATABASE_NAME = os.getenv('DATABASE_NAME')