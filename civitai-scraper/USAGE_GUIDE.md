# Civitai Scraper - מדריך שימוש מהיר

<div dir="rtl">

## הכל מוכן! הנה איך להתחיל:

</div>

## 🎯 Quick Start Options

### Option 1: Interactive Mode (Recommended)
```bash
cd /home/user/Unifai-Data/civitai-scraper
python main.py
```

Then select:
- `1` for API scraping (fast)
- `2` for Web scraping (detailed)
- `3` for both methods

### Option 2: Quick API Test
```bash
cd /home/user/Unifai-Data/civitai-scraper
python quick_api_test.py
```
This tests the API with just 1 page of data.

### Option 3: Python Code
Create your own script:

```python
from api_scraper import CivitaiAPIScraper
from config import API_CONFIG

# Initialize scraper
scraper = CivitaiAPIScraper(api_key=API_CONFIG["api_key"])

# Scrape data
df = scraper.scrape(max_pages=5, fetch_details=False)

# Save results
df.to_excel("./outputs/my_scrape.xlsx", index=False)
print(f"✓ Scraped {len(df)} models!")
```

## 📁 Project Files

```
civitai-scraper/
├── main.py              ← Main script (run this!)
├── quick_api_test.py    ← Quick test
├── api_scraper.py       ← API scraper class
├── web_scraper.py       ← Web scraper class
├── config.py            ← Configuration (edit this!)
├── requirements.txt     ← Dependencies (already installed)
├── README.md            ← Full documentation
├── USAGE_GUIDE.md       ← This file
└── outputs/             ← Results go here
```

## ⚙️ Configuration (config.py)

Edit these settings as needed:

```python
# API Settings
API_CONFIG = {
    "api_key": "9b93f0a5f72d1f7dc8e5aaaabca06ff1",
    "max_pages": 10,          # Change this!
    "limit_per_page": 100,
    "rate_limit_delay": 0.5,
}

# Common Settings
COMMON_CONFIG = {
    "sort": "Highest Rated",  # or "Most Downloaded", "Newest"
    "period": "Month",         # or "AllTime", "Year", "Week", "Day"
    "model_types": None,       # or ["Checkpoint"], ["LORA"], etc.
}
```

## 📊 Output Format

Results are saved in `./outputs/` as:
- **CSV** - For data analysis
- **Excel** - For viewing/editing
- **JSON** - For integration

Example filename: `civitai_api_20250124_153045.xlsx`

## 🔧 Common Scenarios

### Scenario 1: Get top 500 models by downloads
```python
# Edit config.py:
COMMON_CONFIG = {
    "sort": "Most Downloaded",
    "period": "AllTime",
}

# Then run:
python main.py
# Select option 1
```

### Scenario 2: Get only LORA models
```python
# Edit config.py:
COMMON_CONFIG = {
    "model_types": ["LORA"],
}

# Then run:
python main.py
```

### Scenario 3: Get this week's new models
```python
# Edit config.py:
COMMON_CONFIG = {
    "sort": "Newest",
    "period": "Week",
}

# Then run:
python main.py
```

## 🐛 Troubleshooting

### Problem: 503 Service Unavailable

This means Civitai API is temporarily unavailable. Solutions:
1. **Wait 5-10 minutes** and try again
2. **Reduce load**: Set `max_pages: 3` in config.py
3. **Use web scraping**: Run `python main.py` and select option 2

### Problem: API Rate Limit

If you see rate limit errors:
1. Increase `rate_limit_delay` to `1.5` or `2.0` in config.py
2. Reduce `max_pages` to `5` or less
3. Switch to web scraping method

### Problem: Selenium/Chrome Driver Issues

If web scraping fails:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install chromium-chromedriver

# Or disable Selenium in config.py:
SCRAPING_CONFIG = {"use_selenium": False}
```

### Problem: No Results

Check:
1. Internet connection
2. API key in config.py
3. Civitai website is accessible

## 📈 Performance Tips

1. **For speed**: Use API method with `fetch_details=False`
2. **For details**: Use API method with `fetch_details=True`
3. **For flexibility**: Use web scraping method
4. **For testing**: Start with `max_pages=1` or `max_pages=3`

## 🎓 Examples in Different Languages

### Bash Script
```bash
#!/bin/bash
cd /home/user/Unifai-Data/civitai-scraper
python -c "
from api_scraper import CivitaiAPIScraper
from config import API_CONFIG
scraper = CivitaiAPIScraper(API_CONFIG['api_key'])
df = scraper.scrape(max_pages=3)
df.to_csv('./outputs/bash_scrape.csv', index=False)
print('Done!')
"
```

### Jupyter Notebook
```python
import os
os.chdir('/home/user/Unifai-Data/civitai-scraper')

from api_scraper import CivitaiAPIScraper
from config import API_CONFIG

scraper = CivitaiAPIScraper(API_CONFIG["api_key"])
df = scraper.scrape(max_pages=5, fetch_details=False)

# Analyze
print(df.describe())
print(df['type'].value_counts())

# Visualize
df['downloads'].hist(bins=50)
```

## 🚀 Next Steps

<div dir="rtl">

1. **התאם את ההגדרות** ב-`config.py` לצרכים שלך
2. **הרץ סקריפט** עם `python main.py`
3. **בדוק תוצאות** בתיקייה `./outputs/`
4. **נתח נתונים** עם Pandas/Excel
5. **צור סקריפטים מותאמים** לצרכים שלך

</div>

---

## 📞 Need Help?

<div dir="rtl">

- לבעיות טכניות: בדוק את המדריך הזה
- לשאלות על API: ראה [Civitai API Docs](https://github.com/civitai/civitai/wiki/REST-API-Reference)
- לבעיות עם הקוד: פתח issue ב-GitHub

**מערכת מוכנה לשימוש! בהצלחה!** 🎉

</div>
