from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from scraper.database.db_setup import Base

class JobPostings(Base):
    __tablename__ = 'job_postings'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('job_roles.id'))
    job_description = Column(MEDIUMTEXT)
    job_title = Column(String(255))
    company_name = Column(String(255))
    date_scraped = Column(DateTime, default=func.now())

    job_role = relationship('JobRoles', back_populates='jobs')