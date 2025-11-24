# Civitai Scraper - מערכת איסוף נתונים מתקדמת

<div dir="rtl">

## תיאור
Scraper מתקדם למאגר Civitai עם שתי שיטות משלימות:
- **Method 1: API** - מהיר, אמין, עם מגבלות
- **Method 2: Web Scraping** - גמיש, ללא הגבלות (עם Selenium)

</div>

## 📂 Project Structure

```
civitai-scraper/
├── requirements.txt      # Python dependencies
├── config.py            # Configuration settings
├── api_scraper.py       # API-based scraper
├── web_scraper.py       # Web scraping with Selenium
├── main.py              # Main execution script
├── outputs/             # Output directory (CSV, Excel, JSON)
└── README.md            # This file
```

## 🚀 Quick Start

### 1. Installation (Already Done!)

The project is ready to use. All dependencies are installed:
- requests
- beautifulsoup4
- lxml
- selenium
- pandas
- openpyxl
- tqdm

### 2. Run the Scraper

```bash
cd civitai-scraper
python main.py
```

Select your scraping method:
1. **API Only** - Fast and reliable
2. **Web Scraping Only** - More detailed
3. **Both Methods** - Compare results

### 3. View Results

Results are saved in `./outputs/` directory in three formats:
- CSV (for data analysis)
- Excel (for viewing)
- JSON (for integration)

## 📖 Usage Examples

### Example 1: Quick API Scrape

```python
from api_scraper import CivitaiAPIScraper
from config import API_CONFIG

scraper = CivitaiAPIScraper(API_CONFIG["api_key"])
df = scraper.scrape(max_pages=5, fetch_details=False)
df.to_excel("./outputs/quick_api_scrape.xlsx", index=False)
print(f"Done: {len(df)} models scraped")
```

### Example 2: Web Scraping

```python
from web_scraper import CivitaiWebScraper

scraper = CivitaiWebScraper()
df = scraper.scrape(max_pages=3)
df.to_excel("./outputs/quick_web_scrape.xlsx", index=False)
scraper.close()
print(f"Done: {len(df)} models scraped")
```

### Example 3: Detailed API Scrape with Model Info

```python
from api_scraper import CivitaiAPIScraper
from config import API_CONFIG

scraper = CivitaiAPIScraper(API_CONFIG["api_key"])
df = scraper.scrape(max_pages=10, fetch_details=True)
df.to_excel("./outputs/detailed_scrape.xlsx", index=False)
print(f"Scraped {len(df)} models with full details")
```

## ⚙️ Configuration

Edit `config.py` to customize:

### API Settings
- `api_key`: Your Civitai API key
- `max_pages`: Maximum pages to scrape (default: 10)
- `limit_per_page`: Results per page (default: 100)

### Web Scraping Settings
- `use_selenium`: Enable/disable Selenium (default: True)
- `max_pages`: Maximum pages (default: 5)
- `fetch_details`: Fetch model details (default: True)

### Common Settings
- `sort`: "Highest Rated", "Most Downloaded", "Newest"
- `period`: "AllTime", "Year", "Month", "Week", "Day"
- `model_types`: Filter by type (e.g., ["Checkpoint"], ["LORA"])

## 📊 Output Data Fields

### API Method Provides:
- model_id, model_name, model_url
- type, nsfw, tags
- creator_username, creator_image
- downloads, favorites, comments
- rating, rating_count
- description
- latest_version_id, latest_version_name
- base_model, download_url
- trained_words
- file_size_kb, file_format
- image_count, preview_url

### Web Scraping Provides:
- model_id, model_name, model_url
- downloads, favorites
- preview_image
- title, description, tags
- base_model

## 🔄 Method Comparison

| Feature | API | Web Scraping |
|---------|-----|--------------|
| Speed | ⚡⚡⚡ Very Fast | 🐢 Slower |
| Reliability | ✅ High | ⚠️ Medium |
| Data Fields | 📊 Predefined | 🎯 Flexible |
| Setup | 🔑 API Key | 🛠️ Selenium |
| Rate Limits | 1000/day | None |
| Maintenance | ✅ Stable | ⚠️ May need updates |

## 🛠️ Advanced Usage

### Filter by Model Type

Edit `config.py`:
```python
COMMON_CONFIG = {
    "model_types": ["Checkpoint"],  # Only Checkpoint models
    # or ["LORA"], ["Embedding"], etc.
}
```

### Change Sort Order

```python
COMMON_CONFIG = {
    "sort": "Most Downloaded",  # or "Newest", "Highest Rated"
    "period": "Week",  # or "Day", "Month", "Year", "AllTime"
}
```

### Customize Output Directory

```python
COMMON_CONFIG = {
    "output_dir": "./my_custom_outputs",
}
```

## 🐛 Troubleshooting

### Selenium Issues

If web scraping fails:
1. Install Chrome/Chromium driver:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install chromium-chromedriver

   # macOS
   brew install chromedriver
   ```

2. Or disable Selenium in `config.py`:
   ```python
   SCRAPING_CONFIG = {
       "use_selenium": False,
   }
   ```

### API Rate Limits

If you hit API limits:
- Reduce `max_pages` in config
- Increase `rate_limit_delay`
- Use Web Scraping method instead

## 📝 Notes

<div dir="rtl">

- **API Key**: כלול בקובץ config.py (9b93f0a5f72d1f7dc8e5aaaabca06ff1)
- **Rate Limiting**: מובנה במערכת למניעת חסימה
- **Output Formats**: תומך ב-CSV, Excel, JSON
- **Error Handling**: טיפול אוטומטי בשגיאות
- **Progress Tracking**: פס התקדמות בזמן אמת

</div>

## 🎯 Recommended Workflow

1. **Start with API** (fast & reliable):
   ```bash
   python main.py
   # Choose option 1
   ```

2. **Use Web Scraping** for specific needs:
   - When API limits are reached
   - When you need different data fields
   - For testing and validation

3. **Compare both methods** (option 3) to:
   - Validate data accuracy
   - Get complementary information
   - Choose the best method for your use case

## 📄 License

This tool is for educational and research purposes.
Please respect Civitai's Terms of Service and rate limits.

---

<div dir="rtl">

## תמיכה
לשאלות או בעיות, פנה למפתח.

**נבנה עבור Claude Code** - מותאם לסביבת פיתוח CLI

</div>
