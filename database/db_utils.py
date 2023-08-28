from sqlalchemy import text
from database.db_setup import SessionLocal

def create_session():
    return SessionLocal()

def add_instance(session, instance):
    session.add(instance)
    session.commit()


def get_job_descriptions(session):
    results = session.execute(text("SELECT job_description FROM job_postings WHERE job_description IS NOT NULL AND job_description != '';"))
    descriptions = [row[0] for row in results]
    return descriptions