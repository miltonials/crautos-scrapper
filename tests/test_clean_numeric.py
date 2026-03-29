from crautos_scrapper.scraper import CrAutosScraper


class TestCleanNumericValue:
    def test_with_unit(self):
        key, val = CrAutosScraper._clean_numeric_value("Kilometraje", "91,500 kms")
        assert key == "Kilometraje (kms)"
        assert val == 91_500

    def test_with_cc_unit(self):
        key, val = CrAutosScraper._clean_numeric_value("Motor", "2000 cc")
        assert key == "Motor (cc)"
        assert val == 2000

    def test_pure_number(self):
        key, val = CrAutosScraper._clean_numeric_value("Puertas", "4")
        assert key == "Puertas"
        assert val == 4

    def test_non_numeric_string(self):
        key, val = CrAutosScraper._clean_numeric_value("Transmisión", "Automática")
        assert key == "Transmisión"
        assert val == "Automática"

    def test_non_string_value(self):
        key, val = CrAutosScraper._clean_numeric_value("year", 2020)
        assert key == "year"
        assert val == 2020
