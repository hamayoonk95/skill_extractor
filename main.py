import random
import datetime
import os

from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver
# import undetected_chromedriver as uc
import spacy

from constants.user_agents import user_agent_list
from constants.job_roles import job_roles

# Import models and create_session, get_job_descriptions from db_setup and db_utils
from database.db_utils import create_session, add_instance, get_job_descriptions
from database.models.job_posting import JobPostings
from database.models.job_roles import JobRoles
from database.models.role_skills import RoleSkills
from database.models.skill_types import SkillTypes
from database.models.skills import Skills

# import scraper and processor
from scraping.indeed_scraper import IndeedScraper
from processing.data_processor import DataProcessor

from utils.utils import generate_training_data, write_training_data_to_jsonl, load_training_data_from_jsonl
from ner_trainer.train_ner import train_spacy_model


def scrape_and_process_data(session, model_path):
    # load ner model
    model = spacy.load(model_path)
    i = 0
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

        for page_number in range(0, 401, 10):
            job_links = indeed_scraper.indeed_extractor(page_number, role_query)

            for link in job_links:
                scraped_jobs = indeed_scraper.get_job_data(link)
                processed_jobs = indeed_processor.extract_job_data(scraped_jobs)
                print(f"{i}: {processed_jobs}")
                i += 1
                existing_job = session.query(JobPostings).filter_by(
                    job_description=processed_jobs['description']).first()
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

    driver.quit()


def train_ner_model(training_data, model_path, output_dir, n_iter):

    # Record the start time
    start_time = datetime.datetime.now()

    # Train the spaCy model
    nlp = train_spacy_model(training_data=training_data, model_path=model_path, output_dir=output_dir, n_iter=n_iter)
    # Record the end time
    end_time = datetime.datetime.now()

    # Calculate the difference between the end time and start time
    time_diff = end_time - start_time

    print("Training completed in: ", time_diff)


def main():
    # create a new session
    session = create_session()

    # Get action choice from the user
    action = input("What would you like to do? (1: Scrape Data, 2: Train NER Model): ")

    # Initialize paths as None
    json_file_path = None
    model_path = None
    output_dir = None

    if action == '1':
        # Initialize parameters for scraping
        model_path = input("Enter the path to the NER model: ")
        scrape_and_process_data(session, model_path)


    elif action == '2':
        # Initialize parameters for training
        json_file_path = input("Enter the path to your training data JSON file (or press Enter to use a new file): ")
        retrain_option = input("Do you have a pre-existing model you'd like to retrain? (y/n): ")
        if retrain_option.lower() == 'y':
            model_path = input("Enter the path to the existing model: ")

        output_dir = input("Enter the directory where you'd like to save the trained model: ")
        n_iter = int(input("Enter the number of epochs for training: "))

        if json_file_path:
            if not os.path.exists(json_file_path):
                print(f"File {json_file_path} not found. Exiting.")
                return

        if not os.path.exists(json_file_path) or json_file_path == '':
            print("Creating new training data...")
            descriptions = get_job_descriptions(session)
            training_data = [generate_training_data(description) for description in descriptions]
            json_file_path = os.path.join(output_dir, "training_data.jsonl")
            write_training_data_to_jsonl(training_data, json_file_path)

        training_data = load_training_data_from_jsonl(json_file_path)

        train_ner_model(training_data=training_data,model_path=model_path, output_dir=output_dir, n_iter=n_iter)

    else:
        print("Invalid choice. Exiting.")
        return

    session.close()


if __name__ == "__main__":
    main()
