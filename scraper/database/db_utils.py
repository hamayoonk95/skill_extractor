from sqlalchemy import text
from scraper.database.db_setup import SessionLocal

def create_session():
    return SessionLocal()


def add_instance(session, instance):
    session.add(instance)
    session.commit()


def get_job_descriptions(session):
    results = session.execute(text("SELECT job_description FROM job_postings WHERE job_description IS NOT NULL AND job_description != '';"))
    descriptions = [row[0] for row in results]
    return descriptions

from datetime import datetime

def get_recent_job_descriptions(session):
    ten_days_ago = datetime(2023, 11, 25)
    sql = """
        SELECT job_description 
        FROM job_postings
        WHERE 
            job_description IS NOT NULL
            AND job_description != ''
            AND date_scraped > :ten_days_ago
        LIMIT 300
    """

    results = session.execute(text(sql), {'ten_days_ago': ten_days_ago})
    descriptions = [row.job_description for row in results]
    return descriptions