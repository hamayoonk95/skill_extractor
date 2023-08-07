from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship

from database.db_setup import Base

class JobPostings(Base):
    __tablename__ = 'job_postings'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('job_roles.id'))
    job_description = Column(MEDIUMTEXT)
    job_title = Column(String(255))

    job_role = relationship('JobRoles', back_populates='jobs')