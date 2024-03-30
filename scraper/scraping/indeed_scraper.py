import random
import time

from bs4 import BeautifulSoup

class IndeedScraper:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = 'https://uk.indeed.com'

    def indeed_extractor(self, page, role):
        """
                Extract job data from the Indeed page.
                :param role: role_title
                :param page: Page number for job listings.
                :return: page_source from Selenium WebDriver.
        """

        # Define URL
        URL = f"{self.base_url}/jobs?q=Title:({role})&l=UK&start={page}"
        # Navigate to the URL
        self.driver.get(URL)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Find the div containing the job cards
        job_card_div = soup.find('div', id='mosaic-provider-jobcards')
        job_links = set()

        # Find all list items in the job_card div
        if job_card_div is not None:
            job_cards = soup.find_all('li')

            for job in job_cards:
                title_tag = job.find('h2', class_='jobTitle')
                if title_tag:
                    # Find the 'a' tag within the h2 tag
                    title_link = title_tag.find('a')
                    if title_link:
                        job_url = self.base_url + title_link.get('href')
                        job_links.add(job_url)
        return list(job_links)


    def get_job_data(self, job_link):
        self.driver.get(job_link)
        time.sleep(random.randint(1,2))  # delay to prevent getting blocked by the website
        job_data = self.driver.page_source  # store the entire page source
        return job_data

    def is_browser_responsive(self):
        try:
            # Attempt to retrieve the current URL as a responsiveness check
            _ = self.driver.current_url
            print(_)
            return True
        except Exception:
            return False
