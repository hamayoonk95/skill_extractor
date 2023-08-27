import random

from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver
import undetected_chromedriver as uc
import spacy

from constants.user_agents import user_agent_list
from constants.job_roles import job_roles

# Import models and session from db setup
from database.db_setup import create_session, add_instance
from database.models.job_posting import JobPostings
from database.models.job_roles import JobRoles
from database.models.role_skills import RoleSkills
from database.models.skill_types import SkillTypes
from database.models.skills import Skills

from scraping.indeed_scraper import IndeedScraper
from processing.data_processor import DataProcessor


def main():
    # create a new session
    session = create_session()
    model = spacy.load("./ner_model_training/model/epoch_20")
    # Define WebDriver
    options = Options()
    options.add_argument(f"user-agent={random.choice(user_agent_list)}")
    driver = Driver(uc=True)

    indeed_scraper = IndeedScraper(driver)
    indeed_processor = DataProcessor(model)

    for job_role in job_roles:
        role_title = job_role['role_title']
        role_query = job_role['query']

        # Add or get job_role from database
        db_role = session.query(JobRoles).filter_by(role_title=role_title).first()
        if db_role is None:
            db_role = JobRoles(role_title=role_title)
            add_instance(session, db_role)

        # for page_number in range(0, 11, 10):
        job_links = indeed_scraper.indeed_extractor(0, role_query)

        for link in job_links:
            scraped_jobs = indeed_scraper.get_job_data(link)
            processed_jobs = indeed_processor.extract_job_data(scraped_jobs)
            print(processed_jobs)

            existing_job = session.query(JobPostings).filter_by(job_description=processed_jobs['description']).first()
            if existing_job is None:
                job_posting = JobPostings(job_title=processed_jobs['title'],
                                          job_description=processed_jobs['description'],
                                          role_id=db_role.id)
                add_instance(session, job_posting)

            for skill, skill_type in processed_jobs['skills']:
                existing_skill_type = session.query(SkillTypes).filter_by(type_name=skill_type).first()
                if existing_skill_type is None:
                    existing_skill_type = SkillTypes(type_name=skill_type)
                    add_instance(session, existing_skill_type)

                existing_skill = session.query(Skills).filter_by(skill_name=skill).first()
                if existing_skill is None:
                    existing_skill = Skills(skill_name=skill, type_id=existing_skill_type.id)
                    add_instance(session, existing_skill)

                existing_role_skill = session.query(RoleSkills).filter_by(role_id=db_role.id,
                                                                          skill_id=existing_skill.id).first()
                if existing_role_skill:
                    existing_role_skill.frequency += 1
                else:
                    role_skill = RoleSkills(role_id=db_role.id, skill_id=existing_skill.id, frequency=1)
                    add_instance(session, role_skill)

    session.close()
    driver.quit()


if __name__ == "__main__":
    main()
