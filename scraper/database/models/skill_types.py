from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from scraper.database.db_setup import Base

class SkillTypes(Base):
    __tablename__ = 'skill_types'

    id = Column(Integer, primary_key=True)
    type_name = Column(String(50))

    skills = relationship('Skills', back_populates='skill_type')