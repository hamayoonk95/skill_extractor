from datetime import datetime
import spacy

from seleniumbase import get_driver
from fake_useragent import UserAgent

from scraper.database.db_utils import add_instance
from scraper.database.models import JobRole, JobPosting, RoleSkill, SkillType, Skill


def setup_driver():
    ua = UserAgent
    user_agent = ua.random
    # driver = Driver(uc=True, headless=True, agent=user_agent, undetectable=True)
    driver = get_driver("chrome", headless=False, user_agent=user_agent, undetectable=True)
    return driver


def load_ner_model(model_path):
    return spacy.load(model_path)


def get_or_create_job_role(session, role_title):
    db_role = session.query(JobRole).filter_by(role_title=role_title).first()
    if not db_role:
        db_role = JobRole(role_title=role_title)
        add_instance(session, db_role)
    return db_role


def save_job_posting(session, job_data, db_role):
    """
    Save a job posting to the database.
    """
    company_name = job_data.get('company', 'Unknown')

    existing_job = session.query(JobPosting).filter_by(
        job_title=job_data['title'],
        job_description=job_data['description'],
        company_name=company_name,
        role_id=db_role.id
        ).first()
    if not existing_job:
        job_posting = JobPosting(
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
    skill_type = session.query(SkillType).filter_by(type_name=type_name).first()
    if not skill_type:
        skill_type = SkillType(type_name=type_name)
        add_instance(session, skill_type)
    return skill_type


def get_or_create_skill(session, skill_name, skill_type):
    """
    Get an existing skill from the database or create it if it doesn't exist.
    """
    skill = session.query(Skill).filter_by(skill_name=skill_name).first()
    if not skill:
        skill = Skill(skill_name=skill_name, skill_type=skill_type)
        add_instance(session, skill)
    return skill


def get_or_create_role_skill(session, db_role, db_skill):
    """
    Get an existing role-skill relationship from the database or create it if it doesn't exist.
    """

    # Get the current date
    current_date = datetime.utcnow().date()

    role_skill = session.query(RoleSkill).filter_by(
        role_id=db_role.id,
        skill_id=db_skill.id,
        date_scraped=current_date
        ).first()

    if role_skill:
        role_skill.frequency += 1
        session.commit()
    else:
        role_skill = RoleSkill(
            role_id=db_role.id,
            skill_id=db_skill.id,
            frequency=1,
            date_scraped=current_date
            )
        add_instance(session, role_skill)
