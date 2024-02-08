from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from scraper.database.db_setup import Base


# Define the JobRole model
class JobRole(Base):
    __tablename__ = 'job_roles'
    id = Column(Integer, primary_key=True)
    role_title = Column(String(50))
    job_postings = relationship('JobPosting', back_populates='job_role')
    role_skills = relationship('RoleSkill', back_populates='job_role')
    users = relationship('User', back_populates='job_role')
    projects = relationship('Project', back_populates='job_role')

# Define the JobPosting model
class JobPosting(Base):
    __tablename__ = 'job_postings'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('job_roles.id'))
    job_description = Column(Text)
    job_title = Column(String(255))
    company_name = Column(String(255))
    date_scraped = Column(DateTime, default=func.now())
    job_role = relationship('JobRole', back_populates='job_postings')

# Define the SkillType model
class SkillType(Base):
    __tablename__ = 'skill_types'
    id = Column(Integer, primary_key=True)
    type_name = Column(String(50))
    skills = relationship('Skill', back_populates='skill_type')

# Define the Skill model
class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    skill_name = Column(String(255))
    type_id = Column(Integer, ForeignKey('skill_types.id'))
    skill_type = relationship('SkillType', back_populates='skills')
    role_skills = relationship('RoleSkill', back_populates='skill')
    # user_skills = relationship('UserSkill', back_populates='skill')

# Define the RoleSkill model
class RoleSkill(Base):
    __tablename__ = 'role_skills'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('job_roles.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    frequency = Column(Integer)

    job_role = relationship('JobRole', back_populates='role_skills')
    skill = relationship('Skill', back_populates='role_skills')

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    jobrole_id = Column(Integer, ForeignKey('job_roles.id'))
    firstname = Column(String(50))
    lastname = Column(String(50))
    username = Column(String(50))
    email = Column(String(255))
    password = Column(String(255))
    # user_skills = relationship('UserSkill', back_populates='user')
    job_role = relationship('JobRole', back_populates='users')
    projects = relationship('Project', back_populates='user')

# Define the Project model
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    role_id = Column(Integer, ForeignKey('job_roles.id'))
    user = relationship('User', back_populates='projects')
    job_role = relationship('JobRole', back_populates='projects')