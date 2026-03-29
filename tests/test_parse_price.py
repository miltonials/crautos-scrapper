from crautos_scrapper.scraper import CrAutosScraper


class TestParsePrice:
    def test_colones_first(self):
        content = "&cent; 6,800,000 $ 11,500"
        result = CrAutosScraper._parse_price(content)
        assert result["colones"] == 6_800_000
        assert result["dolares"] == 11_500

    def test_dollars_first(self):
        content = "$ 11,500 &cent; 6,800,000"
        result = CrAutosScraper._parse_price(content)
        assert result["dolares"] == 11_500
        assert result["colones"] == 6_800_000

    def test_no_prices(self):
        result = CrAutosScraper._parse_price("no price here")
        assert result["colones"] is None
        assert result["dolares"] is None

    def test_single_price_returns_none(self):
        result = CrAutosScraper._parse_price("$ 11,500")
        assert result["colones"] is None
        assert result["dolares"] is None

    def test_large_values(self):
        content = "&cent; 25,000,000 $ 42,000"
        result = CrAutosScraper._parse_price(content)
        assert result["colones"] == 25_000_000
        assert result["dolares"] == 42_000
