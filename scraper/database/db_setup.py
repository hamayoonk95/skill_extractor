from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from scraper.database.config import DRIVER_NAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, DATABASE_NAME

# Create an engine without a database
engine_without_db = create_engine(
    URL.create(
        drivername=DRIVER_NAME,
        username=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
    )
)

# Create the database if it doesn't exist
with engine_without_db.connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))

url = URL.create(
    drivername=DRIVER_NAME,
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    database=DATABASE_NAME
)

db_engine = create_engine(url)

# Create SQLAlchemy session bound to the database engine
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=db_engine)

# Base class for declarative model definitions
Base = declarative_base()


# Import trained_models after the Base has been created
from scraper.database.models import job_roles
from scraper.database.models import job_posting
from scraper.database.models import skills
from scraper.database.models import skill_types
from scraper.database.models import role_skills

# Create all the trained_models in the database
Base.metadata.create_all(bind=db_engine)