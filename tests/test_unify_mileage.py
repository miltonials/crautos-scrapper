import pandas as pd
import pytest

from crautos_scrapper.scraper import CrAutosScraper


class TestUnifyMileage:
    def setup_method(self):
        self.scraper = CrAutosScraper(max_concurrent_requests=1)

    def test_only_kms(self):
        df = pd.DataFrame({"Kilometraje (kms)": [100_000]})
        result = self.scraper._unify_mileage(df)
        assert result["Kilometraje (kms)"].iloc[0] == 100_000
        assert result["Kilometraje (millas)"].iloc[0] == pytest.approx(100_000 / 1.60934, rel=1e-3)

    def test_only_millas(self):
        df = pd.DataFrame({"Kilometraje (millas)": [60_000]})
        result = self.scraper._unify_mileage(df)
        assert result["Kilometraje (millas)"].iloc[0] == 60_000
        assert result["Kilometraje (kms)"].iloc[0] == pytest.approx(60_000 * 1.60934, rel=1e-3)

    def test_both_present(self):
        df = pd.DataFrame({"Kilometraje (kms)": [100_000], "Kilometraje (millas)": [62_137]})
        result = self.scraper._unify_mileage(df)
        assert result["Kilometraje (kms)"].iloc[0] == 100_000
        assert result["Kilometraje (millas)"].iloc[0] == 62_137

    def test_neither_present(self):
        df = pd.DataFrame({"name": ["test"]})
        result = self.scraper._unify_mileage(df)
        assert result["Kilometraje (kms)"].iloc[0] == 0
        assert result["Kilometraje (millas)"].iloc[0] == 0
