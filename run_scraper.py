"""Runner script for the CrAutos scraper.

Handles the module import for crautos-scrapper.py (which cannot be
imported directly due to the hyphen in the filename) and executes
the scraper with conservative parameters.
"""
import asyncio
import importlib.util
import os
import sys
from pathlib import Path


def load_scraper_module():
    """Load crautos-scrapper.py as a module despite the hyphen in its name."""
    spec = importlib.util.spec_from_file_location(
        "scraper",
        Path(__file__).parent / "crautos-scrapper.py",
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["scraper"] = module
    spec.loader.exec_module(module)
    return module


async def main():
    scraper_module = load_scraper_module()

    total_pages = int(os.environ.get("TOTAL_PAGES", "3"))
    max_concurrent = int(os.environ.get("MAX_CONCURRENT", "5"))

    scraper = scraper_module.CrAutosScraper(max_concurrent_requests=max_concurrent)
    df = await scraper.run(total_pages=total_pages)

    if df.empty:
        print("No data was scraped. The site may be unreachable.")
        sys.exit(1)

    print(f"Scraped {len(df)} car listings.")
    print(df.head())
    df.to_csv("crautos_dataset.csv", index=False, encoding="utf-8-sig")
    print("Saved to crautos_dataset.csv")


if __name__ == "__main__":
    asyncio.run(main())
