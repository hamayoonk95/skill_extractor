from unittest.mock import Mock
from scraper.scraping.indeed_scraper import IndeedScraper
from tests.test_helpers import read_sample_html

mock_driver = Mock()

# Initialize scraper object
scraper = IndeedScraper(mock_driver)
role = 'Software Developer'
page = 0
job_link = 'https://uk.indeed.com/some_job_link'


def test_indeed_extractor_no_job_card():
    """
    Edge case: Test what happens when no job card div is found
    """
    # Read the sample HTML and set it as the page source for the mock driver
    mock_driver.page_source = read_sample_html('./html_templates/no_job_card.html')

    # Call the actual function (no need to mock BeautifulSoup this time)
    result = scraper.indeed_extractor(page, role)

    # Validate the function's output
    assert result == []


def test_indeed_extractor_with_job_cards():
    """
    Edge case: Test what happens when job cards are found
    """
    # Read the sample HTML and set it as the page source for the mock driver
    mock_driver.page_source = read_sample_html('./html_templates/with_job_cards.html')

    # Call the indeed_extractor to get links out of the page
    result = scraper.indeed_extractor(page, role)
    result = sorted(result)
    # Validate the function's output
    expected_links = ['https://uk.indeed.com/some_path1', 'https://uk.indeed.com/some_path2']
    expected_links = sorted(expected_links)
    assert result == expected_links



def test_get_job_data():
    """
    General test for get_job_data, when everything works as normal
    """
    mock_driver.page_source = read_sample_html('./html_templates/job_data.html')
    # call get_job_data with mock link to check if it returns the right output
    result = scraper.get_job_data(job_link)
    assert result == mock_driver.page_source
