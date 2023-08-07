from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.db_setup import Base


class RoleSkills(Base):
    __tablename__ = 'role_skills'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('job_roles.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    frequency = Column(Integer)

    # Relationships
    job_role = relationship("JobRoles", back_populates="role_skills")
    skill = relationship("Skills", back_populates="role_skills")
