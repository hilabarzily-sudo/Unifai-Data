"""
Civitai API Scraper
Method 1: Using official Civitai API
"""

import requests
import pandas as pd
from typing import Dict, List, Optional
import time
from tqdm import tqdm
import json
import os
from config import API_CONFIG, COMMON_CONFIG


class CivitaiAPIScraper:
    """Scraper using Civitai official API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = API_CONFIG["base_url"]
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })

    def get_models(self, max_pages: Optional[int] = None) -> List[Dict]:
        """Fetch models from API"""
        all_models = []
        page = 1
        cursor = None

        params = {
            "limit": API_CONFIG["limit_per_page"],
            "sort": COMMON_CONFIG["sort"],
            "period": COMMON_CONFIG["period"],
        }

        if COMMON_CONFIG["model_types"]:
            params["types"] = COMMON_CONFIG["model_types"]

        max_pages = max_pages or API_CONFIG["max_pages"]

        print(f"\n{'='*60}")
        print("CIVITAI API SCRAPER")
        print(f"{'='*60}")
        print(f"Max pages: {max_pages}")
        print(f"Sort: {params['sort']}")
        print(f"Period: {params['period']}")
        print(f"{'='*60}\n")

        with tqdm(desc="Fetching via API", unit="page") as pbar:
            while page <= max_pages:
                # Use cursor for pagination
                if cursor:
                    params["cursor"] = cursor
                elif "cursor" in params:
                    del params["cursor"]

                try:
                    response = self.session.get(
                        f"{self.base_url}/models",
                        params=params,
                        timeout=30
                    )
                    response.raise_for_status()
                    data = response.json()

                    items = data.get("items", [])
                    if not items:
                        break

                    all_models.extend(items)
                    pbar.update(1)
                    pbar.set_postfix({"Total": len(all_models)})

                    metadata = data.get("metadata", {})
                    # Get nextCursor for next page
                    cursor = metadata.get("nextCursor")
                    if not cursor:
                        break

                    page += 1
                    time.sleep(API_CONFIG["rate_limit_delay"])

                except requests.exceptions.RequestException as e:
                    print(f"Error on page {page}: {e}")
                    break

        return all_models

    def get_model_details(self, model_id: int) -> Optional[Dict]:
        """Fetch detailed model information"""
        try:
            response = self.session.get(
                f"{self.base_url}/models/{model_id}",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching model {model_id}: {e}")
            return None

    def enrich_with_details(self, models: List[Dict]) -> List[Dict]:
        """Add detailed information to models"""
        enriched = []

        print("\nFetching detailed information...")
        for model in tqdm(models, desc="Model details"):
            model_id = model.get("id")
            if model_id:
                details = self.get_model_details(model_id)
                if details:
                    enriched.append({**model, **details})
                time.sleep(API_CONFIG["rate_limit_delay"])

        return enriched

    def to_dataframe(self, models: List[Dict]) -> pd.DataFrame:
        """Convert models to structured DataFrame"""
        records = []

        for model in models:
            record = {
                "model_id": model.get("id"),
                "model_name": model.get("name"),
                "model_url": f"https://civitai.com/models/{model.get('id')}",
                "type": model.get("type"),
                "nsfw": model.get("nsfw"),
                "creator_username": model.get("creator", {}).get("username"),
                "creator_image": model.get("creator", {}).get("image"),
                "downloads": model.get("stats", {}).get("downloadCount", 0),
                "favorites": model.get("stats", {}).get("favoriteCount", 0),
                "comments": model.get("stats", {}).get("commentCount", 0),
                "rating": model.get("stats", {}).get("rating", 0),
                "rating_count": model.get("stats", {}).get("ratingCount", 0),
                "description": str(model.get("description", ""))[:500],
                "tags": ", ".join(model.get("tags", [])),
                "version_count": len(model.get("modelVersions", [])),
            }

            # Latest version details
            versions = model.get("modelVersions", [])
            if versions:
                latest = versions[0]
                record.update({
                    "latest_version_id": latest.get("id"),
                    "latest_version_name": latest.get("name"),
                    "base_model": latest.get("baseModel"),
                    "download_url": latest.get("downloadUrl"),
                    "trained_words": ", ".join(latest.get("trainedWords", [])),
                })

                # File info
                files = latest.get("files", [])
                if files:
                    main_file = files[0]
                    record.update({
                        "file_size_kb": main_file.get("sizeKB", 0),
                        "file_format": main_file.get("type"),
                    })

                # Images
                images = latest.get("images", [])
                record["image_count"] = len(images)
                if images:
                    record["preview_url"] = images[0].get("url")

            records.append(record)

        return pd.DataFrame(records)

    def scrape(self, max_pages: Optional[int] = None,
               fetch_details: bool = False) -> pd.DataFrame:
        """Main scraping method"""
        models = self.get_models(max_pages)
        print(f"\n✓ Fetched {len(models)} models via API")

        if fetch_details:
            models = self.enrich_with_details(models)
            print(f"✓ Enriched with detailed information")

        df = self.to_dataframe(models)
        return df
