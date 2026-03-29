from crautos_scrapper.scraper import CrAutosScraper


class TestProcessResults:
    def setup_method(self):
        self.scraper = CrAutosScraper(max_concurrent_requests=1)

    def test_valid_results(self):
        results = [
            ("123", "2020&nbsp;"),
            ("123", ""),
            ("123", "Toyota Corolla"),
            ("123", "&cent; 6,800,000 $ 11,500"),
        ]
        cars = self.scraper._process_results(results)
        assert len(cars) == 1
        assert cars[0].id == "123"
        assert cars[0].name == "Toyota Corolla"
        assert cars[0].year == 2020
        assert cars[0].CRC == 6_800_000
        assert cars[0].USD == 11_500

    def test_destacado_filtered(self):
        results = [
            ("123", "2020&nbsp;"),
            ("123", ""),
            ("123", "Destacado Premium"),
            ("123", "&cent; 6,800,000 $ 11,500"),
        ]
        cars = self.scraper._process_results(results)
        assert len(cars) == 0

    def test_clasificados_filtered(self):
        results = [
            ("123", "2020&nbsp;"),
            ("123", ""),
            ("123", "Clasificados especiales"),
            ("123", "&cent; 6,800,000 $ 11,500"),
        ]
        cars = self.scraper._process_results(results)
        assert len(cars) == 0

    def test_empty_results(self):
        assert self.scraper._process_results([]) == []

    def test_insufficient_results(self):
        results = [("123", "data"), ("456", "data")]
        assert self.scraper._process_results(results) == []
