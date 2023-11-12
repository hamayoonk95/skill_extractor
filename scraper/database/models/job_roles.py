from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from scraper.database.db_setup import Base

class JobRoles(Base):
    __tablename__ = 'job_roles'

    id = Column(Integer, primary_key=True)
    role_title = Column(String(50))

    jobs = relationship('JobPostings', back_populates='job_role')
    role_skills = relationship("RoleSkills", back_populates="job_role")