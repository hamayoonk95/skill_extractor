from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from scraper.database.db_setup import Base


class Skills(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    skill_name = Column(String(255))
    type_id = Column(Integer, ForeignKey('skill_types.id'))

    # Relationships
    skill_type = relationship("SkillTypes", back_populates="skills")
    role_skills = relationship("RoleSkills", back_populates="skill")