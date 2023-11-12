import random
import spacy
from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver

from constants.user_agents import user_agent_list

from scraper.database.db_utils import add_instance
from scraper.database.models.job_posting import JobPostings
from scraper.database.models.job_roles import JobRoles
from scraper.database.models.role_skills import RoleSkills
from scraper.database.models.skill_types import SkillTypes
from scraper.database.models.skills import Skills


def setup_driver():
    options = Options()
    options.add_argument(f"user-agent={random.choice(user_agent_list)}")
    driver = Driver(uc=True)
    return driver


def load_ner_model(model_path):
    return spacy.load(model_path)


def get_or_create_job_role(session, role_title):
    db_role = session.query(JobRoles).filter_by(role_title=role_title).first()
    if not db_role:
        db_role = JobRoles(role_title=role_title)
        add_instance(session, db_role)
    return db_role


def save_job_posting(session, job_data, db_role):
    """
    Save a job posting to the database.
    """
    company_name = job_data.get('company', 'Unknown')

    existing_job = session.query(JobPostings).filter_by(
        job_title=job_data['title'],
        job_description=job_data['description'],
        company_name=company_name
        ).first()
    if not existing_job:
        job_posting = JobPostings(
            job_title=job_data['title'],
            job_description=job_data['description'],
            company_name=company_name,
            role_id=db_role.id
            )
        add_instance(session, job_posting)
        save_skills(session, job_data['skills'], db_role)


def save_skills(session, skills_data, db_role):
    """
    Save skills and their relationship to job roles in the database.
    """
    for skill_name, skill_type_name in skills_data:
        skill_type = get_or_create_skill_type(session, skill_type_name)
        skill = get_or_create_skill(session, skill_name, skill_type)
        get_or_create_role_skill(session, db_role, skill)


def get_or_create_skill_type(session, type_name):
    """
    Get an existing skill type from the database or create it if it doesn't exist.
    """
    skill_type = session.query(SkillTypes).filter_by(type_name=type_name).first()
    if not skill_type:
        skill_type = SkillTypes(type_name=type_name)
        add_instance(session, skill_type)
    return skill_type


def get_or_create_skill(session, skill_name, skill_type):
    """
    Get an existing skill from the database or create it if it doesn't exist.
    """
    skill = session.query(Skills).filter_by(skill_name=skill_name).first()
    if not skill:
        skill = Skills(skill_name=skill_name, skill_type=skill_type)
        add_instance(session, skill)
    return skill


def get_or_create_role_skill(session, db_role, db_skill):
    """
    Get an existing role-skill relationship from the database or create it if it doesn't exist.
    """
    role_skill = session.query(RoleSkills).filter_by(role_id=db_role.id, skill_id=db_skill.id).first()
    if role_skill:
        role_skill.frequency += 1
        session.commit()
    else:
        role_skill = RoleSkills(role_id=db_role.id, skill_id=db_skill.id, frequency=1)
        add_instance(session, role_skill)
