import asyncio
import os
import sys

from crautos_scrapper.scraper import CrAutosScraper


def main():
    total_pages = int(os.environ.get("TOTAL_PAGES", "3"))
    max_concurrent = int(os.environ.get("MAX_CONCURRENT", "5"))

    scraper = CrAutosScraper(max_concurrent_requests=max_concurrent)
    df = asyncio.run(scraper.run(total_pages=total_pages))

    if df.empty:
        print("No data was scraped. The site may be unreachable.")
        sys.exit(1)

    print(f"Scraped {len(df)} car listings.")
    print(df.head())
    df.to_csv("crautos_dataset.csv", index=False, encoding="utf-8-sig")
    print("Saved to crautos_dataset.csv")


if __name__ == "__main__":
    main()
