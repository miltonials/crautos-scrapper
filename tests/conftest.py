import pytest

from crautos_scrapper.scraper import CrAutosScraper


@pytest.fixture
def scraper():
    return CrAutosScraper(max_concurrent_requests=1)
