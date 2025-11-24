"""
Quick API Test - Test Civitai API connection and scrape 1 page
"""

from api_scraper import CivitaiAPIScraper
from config import API_CONFIG
import pandas as pd

def quick_test():
    """Quick test with 1 page of data"""
    print("="*60)
    print("CIVITAI API - QUICK TEST")
    print("="*60)
    print("Testing API connection with 1 page of data...\n")

    try:
        scraper = CivitaiAPIScraper(api_key=API_CONFIG["api_key"])
        df = scraper.scrape(max_pages=1, fetch_details=False)

        if len(df) > 0:
            print("\n✓ SUCCESS! API is working")
            print(f"✓ Retrieved {len(df)} models")
            print(f"✓ Columns: {list(df.columns)}")
            print(f"\nSample data:")
            print(df[['model_name', 'downloads', 'rating']].head(5))

            # Save test output
            df.to_csv("./outputs/api_test.csv", index=False)
            print(f"\n✓ Test results saved to: ./outputs/api_test.csv")
        else:
            print("\n⚠ No data retrieved. Check your API key or internet connection.")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify API key in config.py")
        print("3. Check if Civitai API is accessible")

if __name__ == "__main__":
    quick_test()
