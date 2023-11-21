from scraper.scraper_utils import (
    setup_driver, load_ner_model, get_or_create_job_role,
    save_job_posting)

from scraper.database.db_utils import create_session
from scraper.scraping.indeed_scraper import IndeedScraper
from scraper.scraping.data_processor import DataProcessor
from constants.job_roles import job_roles


def main():
    # Set up the database session
    session = create_session()

    # Set up the driver
    driver = setup_driver()

    # Load the NER model
    model_path = input("Enter the path to the NER model: ")
    ner_model = load_ner_model(model_path)

    # Initialize the scraper and processor
    indeed_scraper = IndeedScraper(driver)
    indeed_processor = DataProcessor(ner_model)

    job_count = 0

    try:
        # Perform scraping and processing for each job role
        for job_role in job_roles:
            # get job role title and query from constants
            role_title = job_role['role_title']
            role_query = job_role['query']

            # Add or get job_role from database
            db_role = get_or_create_job_role(session, role_title)

            # Scrape job links for the current role query
            for page_number in range(0, 401, 10):
                # scrapes page from indeed with custom query search for each role
                job_links = indeed_scraper.indeed_extractor(page_number, role_query)

                # Process each job link
                for link in job_links:
                    job_data = indeed_scraper.get_job_data(link)
                    processed_job_data = indeed_processor.extract_job_data(job_data)

                    # Increment the job count
                    job_count += 1
                    print(f"Job {job_count}: {processed_job_data['title']}")
                    print(f"Description: {processed_job_data['description'][:200]}...")

                    # Save the processed job posting to the database
                    job_posting = save_job_posting(session, processed_job_data, db_role)
    finally:
        # Clean up the driver and session
        driver.quit()
        session.close()


if __name__ == "__main__":
    main()
