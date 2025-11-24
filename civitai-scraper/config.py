"""
Configuration file for Civitai Scraper
"""

# API Configuration
API_CONFIG = {
    "api_key": "9b93f0a5f72d1f7dc8e5aaaabca06ff1",
    "base_url": "https://civitai.com/api/v1",
    "max_pages": 10,
    "limit_per_page": 100,
    "rate_limit_delay": 0.5,
}

# Web Scraping Configuration
SCRAPING_CONFIG = {
    "use_selenium": True,
    "max_pages": 5,
    "fetch_details": True,
    "rate_limit_delay": 2,
    "checkpoint_interval": 50,
}

# Common Settings
COMMON_CONFIG = {
    "sort": "Highest Rated",  # Options: Highest Rated, Most Downloaded, Newest
    "period": "Month",  # Options: AllTime, Year, Month, Week, Day
    "model_types": None,  # Options: None, ["Checkpoint"], ["LORA"], etc.
    "output_dir": "./outputs",
}

# User Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
