"""
Main execution file for Civitai Scraper
Supports both API and Web Scraping methods
"""

import os
import pandas as pd
from datetime import datetime
from api_scraper import CivitaiAPIScraper
from web_scraper import CivitaiWebScraper
from config import API_CONFIG, SCRAPING_CONFIG, COMMON_CONFIG


def ensure_output_dir():
    """Create output directory"""
    os.makedirs(COMMON_CONFIG["output_dir"], exist_ok=True)


def save_results(df: pd.DataFrame, method: str):
    """Save scraping results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = f"{COMMON_CONFIG['output_dir']}/civitai_{method}_{timestamp}"

    # Save formats
    df.to_csv(f"{base_path}.csv", index=False, encoding='utf-8-sig')
    df.to_excel(f"{base_path}.xlsx", index=False, engine='openpyxl')
    df.to_json(f"{base_path}.json", orient='records', force_ascii=False, indent=2)

    print(f"\n✓ Saved to:")
    print(f"  - {base_path}.csv")
    print(f"  - {base_path}.xlsx")
    print(f"  - {base_path}.json")

    return base_path


def print_summary(df: pd.DataFrame):
    """Print data summary"""
    print(f"\n{'='*60}")
    print("DATA SUMMARY")
    print(f"{'='*60}")
    print(f"Total models: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nColumns:")
    for col in df.columns:
        print(f"  - {col}")

    print(f"\nFirst 3 rows:")
    print(df.head(3).to_string())

    if 'downloads' in df.columns:
        print(f"\nTop 5 by downloads:")
        top5 = df.nlargest(5, 'downloads')[['model_name', 'downloads', 'model_url']]
        print(top5.to_string(index=False))


def scrape_via_api(fetch_details: bool = False):
    """Method 1: Scrape using API"""
    print("\n" + "="*60)
    print("METHOD 1: API SCRAPING")
    print("="*60)

    scraper = CivitaiAPIScraper(api_key=API_CONFIG["api_key"])
    df = scraper.scrape(
        max_pages=API_CONFIG["max_pages"],
        fetch_details=fetch_details
    )

    save_results(df, "api")
    print_summary(df)

    return df


def scrape_via_web():
    """Method 2: Scrape using HTML"""
    print("\n" + "="*60)
    print("METHOD 2: WEB SCRAPING")
    print("="*60)

    scraper = CivitaiWebScraper()

    try:
        df = scraper.scrape(max_pages=SCRAPING_CONFIG["max_pages"])
        save_results(df, "web")
        print_summary(df)
        return df

    finally:
        scraper.close()


def scrape_both_methods():
    """Run both methods and compare"""
    print("\n" + "="*60)
    print("RUNNING BOTH METHODS")
    print("="*60)

    # Method 1: API
    df_api = scrape_via_api(fetch_details=False)

    # Method 2: Web
    df_web = scrape_via_web()

    # Comparison
    print(f"\n{'='*60}")
    print("COMPARISON")
    print(f"{'='*60}")
    print(f"API results: {len(df_api)} models")
    print(f"Web results: {len(df_web)} models")

    return df_api, df_web


if __name__ == "__main__":
    ensure_output_dir()

    print("""
╔════════════════════════════════════════════════════════════╗
║           CIVITAI SCRAPER - DUAL METHOD                    ║
╚════════════════════════════════════════════════════════════╝

Select scraping method:
1. API Only (fast, reliable)
2. Web Scraping Only (detailed)
3. Both Methods (comparison)
    """)

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        scrape_via_api(fetch_details=True)

    elif choice == "2":
        scrape_via_web()

    elif choice == "3":
        scrape_both_methods()

    else:
        print("Invalid choice. Running API method by default.")
        scrape_via_api(fetch_details=False)

    print("\n✓ Scraping complete!")
