from crautos_scrapper.scraper import CrAutosScraper


class TestParseYear:
    def test_standard_year(self):
        assert CrAutosScraper._parse_year("2020&nbsp;Toyota Corolla") == 2020

    def test_no_year(self):
        assert CrAutosScraper._parse_year("Toyota Corolla") == 0

    def test_multiple_years_returns_last(self):
        assert CrAutosScraper._parse_year("2018&nbsp;some text 2020&nbsp;") == 2020

    def test_year_not_followed_by_nbsp(self):
        assert CrAutosScraper._parse_year("2020 Toyota") == 0
