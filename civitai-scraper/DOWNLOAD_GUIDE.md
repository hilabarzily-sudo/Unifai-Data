# Civitai Image & Prompt Downloader - מדריך שימוש

## ✅ מה כבר הורדנו?

**סיימנו להוריד בהצלחה:**
- ✨ **100 מודלים** (המודלים הפופולריים ביותר)
- ✨ **993 תמונות** באיכות מלאה
- ✨ **993 פרומפטים** + metadata
- ✨ **2.8 GB** נתונים מאורגנים
- ✨ **0 שגיאות**

הכל מאורגן ב-`./downloads/` לפי תיקיות מודלים.

---

## 📂 מבנה התיקיות

```
downloads/
├── CyberRealistic Pony/
│   ├── model_info.json          ← מידע על המודל
│   ├── images/                  ← כל התמונות
│   │   ├── image_001_0.jpg
│   │   ├── image_002_1.png
│   │   └── ...
│   └── prompts/                 ← פרומפטים + metadata
│       ├── image_001_0_prompt.txt
│       ├── image_001_0_metadata.json
│       └── ...
├── Nova Anime XL/
├── PerfectDeliberate/
└── ... (100 מודלים)
```

---

## 🚀 איך להמשיך להוריד?

### אופציה 1: הורד עוד 100 מודלים

```bash
cd /home/user/Unifai-Data/civitai-scraper

# ערוך את הקובץ run_full_download.py
# שנה: max_models = 100  →  max_models = 200

# הרץ:
python run_full_download.py
```

זה יוריד מודלים 101-200 (עוד 100 מודלים).

### אופציה 2: הורד הכל (2,000 מודלים)

```bash
# ערוך run_full_download.py:
max_models = 2000  # במקום 100
max_images_per_model = 10

# הרץ:
python run_full_download.py
```

**⚠️ זה ייקח:**
- זמן: ~5-6 שעות
- מקום: ~50-60 GB
- תמונות: ~20,000

### אופציה 3: הורד רק מודלים ספציפיים

```python
from image_downloader import CivitaiImageDownloader
import pandas as pd

# טען נתונים
df = pd.read_csv('./outputs/civitai_fixed_20251124_161134.csv')

# סנן לפי קריטריון (לדוגמה: רק LORA)
lora_models = df[df['type'] == 'LORA']

# שמור לקובץ זמני
lora_models.to_csv('./temp_lora.csv', index=False)

# הורד
downloader = CivitaiImageDownloader(output_dir='./downloads_lora')
downloader.download_from_csv(
    csv_path='./temp_lora.csv',
    max_models=50,
    max_images_per_model=10
)
```

### אופציה 4: הורד רק מודלים עם הרבה הורדות

```python
import pandas as pd
from image_downloader import CivitaiImageDownloader

# טען נתונים
df = pd.read_csv('./outputs/civitai_fixed_20251124_161134.csv')

# רק מודלים עם 10,000+ הורדות
popular = df[df['downloads'] >= 10000]
popular.to_csv('./temp_popular.csv', index=False)

# הורד
downloader = CivitaiImageDownloader(output_dir='./downloads_popular')
downloader.download_from_csv('./temp_popular.csv', max_models=200)
```

---

## 🎛️ הגדרות מתקדמות

### שנה כמה תמונות לכל מודל

ב-`run_full_download.py`:
```python
max_images_per_model = 20  # במקום 10
```

### שנה תיקיית פלט

ב-`run_full_download.py`:
```python
output_dir = "./my_custom_downloads"
```

### הרץ בפורמט שונה

```bash
# הרץ בסקריפט Python ישיר
python -c "
from image_downloader import CivitaiImageDownloader

downloader = CivitaiImageDownloader(output_dir='./downloads')
downloader.download_from_csv(
    csv_path='./outputs/civitai_fixed_20251124_161134.csv',
    max_models=50,
    max_images_per_model=15
)
"
```

---

## 📊 נתח את התמונות שהורדת

### ספור תמונות לפי מודל

```bash
for dir in downloads/*/; do
    count=$(ls "$dir/images/" 2>/dev/null | wc -l)
    echo "$count images in: $(basename "$dir")"
done | sort -rn | head -20
```

### מצא פרומפטים עם תוכן

```bash
find downloads/ -name "*_prompt.txt" -size +100c -exec echo {} \; -exec cat {} \; -exec echo "---" \;
```

### יצא רשימת כל המודלים שהורדת

```bash
ls -1 downloads/ > downloaded_models_list.txt
```

---

## 🔧 פתרון בעיות

### שגיאת SSL

אם אתה מקבל שגיאות SSL:
```python
# הוסף לתחילת image_downloader.py:
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### אין מקום בדיסק

בדוק כמה מקום יש:
```bash
df -h .
```

נקה קבצים ישנים:
```bash
rm -rf downloads_test/
rm -f download_log.txt
```

### ההורדה נעצרה

אם ההורדה נעצרה באמצע:
1. הסקריפט דולג אוטומטית על קבצים קיימים
2. פשוט הרץ שוב את אותו פקודה - זה ימשיך מאיפה שעצר

---

## 📈 השוואת שיטות הורדה

| תכונה | 100 מודלים | 500 מודלים | 2,000 מודלים |
|-------|------------|------------|---------------|
| זמן | ~13 דקות | ~1 שעה | ~5-6 שעות |
| מקום | ~3 GB | ~15 GB | ~60 GB |
| תמונות | ~1,000 | ~5,000 | ~20,000 |
| מומלץ | ✅ מושלם לבדיקה | ✅ מאזן טוב | ⚠️ רק אם יש מקום |

---

## 🎯 תרחישים נפוצים

### 1. אני רוצה רק Checkpoints

```python
import pandas as pd
from image_downloader import CivitaiImageDownloader

df = pd.read_csv('./outputs/civitai_fixed_20251124_161134.csv')
checkpoints = df[df['type'] == 'Checkpoint']
checkpoints.to_csv('./temp_checkpoints.csv', index=False)

downloader = CivitaiImageDownloader(output_dir='./downloads_checkpoints')
downloader.download_from_csv('./temp_checkpoints.csv', max_models=100)
```

### 2. אני רוצה רק Illustrious models

```python
df = pd.read_csv('./outputs/civitai_fixed_20251124_161134.csv')
illustrious = df[df['base_model'] == 'Illustrious']
illustrious.to_csv('./temp_illustrious.csv', index=False)

downloader = CivitaiImageDownloader(output_dir='./downloads_illustrious')
downloader.download_from_csv('./temp_illustrious.csv')
```

### 3. אני רוצה המשך מאיפה שעצרתי

פשוט הרץ שוב:
```bash
python run_full_download.py
```

המערכת דולגת אוטומטית על קבצים קיימים!

---

## 📝 הערות חשובות

1. **פרומפטים ריקים**: חלק מהתמונות ב-Civitai לא כוללות פרומפטים. זה נורמלי.

2. **Rate Limiting**: יש delay של 0.3 שניות בין כל תמונה כדי לא להכביד על השרת.

3. **שמירה**: כל תמונה נשמרת עם:
   - הקובץ המקורי (jpg/png/webp)
   - קובץ prompt.txt
   - קובץ metadata.json

4. **גיבוי**: מומלץ לגבות את התיקייה `downloads/` אחרי הורדה גדולה.

---

## 🎨 דוגמאות שימוש

### יצא Excel של כל התמונות שהורדת

```python
import pandas as pd
import os

data = []
for model_dir in os.listdir('downloads/'):
    model_path = f'downloads/{model_dir}'
    if not os.path.isdir(model_path):
        continue

    # ספור תמונות
    images_dir = f'{model_path}/images'
    if os.path.exists(images_dir):
        image_count = len(os.listdir(images_dir))
        data.append({
            'model': model_dir,
            'images': image_count
        })

df = pd.DataFrame(data)
df = df.sort_values('images', ascending=False)
df.to_excel('downloads_summary.xlsx', index=False)
print(f"Saved summary for {len(df)} models")
```

### מצא מודלים עם פרומפטים

```bash
# מצא מודלים עם פרומפטים לא ריקים
for dir in downloads/*/prompts/; do
    non_empty=$(find "$dir" -name "*_prompt.txt" -size +100c | wc -l)
    if [ $non_empty -gt 0 ]; then
        echo "$(basename $(dirname $dir)): $non_empty prompts with content"
    fi
done
```

---

## 🎉 סיכום

**יש לך עכשיו:**
- ✅ 100 מודלים עם תמונות ופרומפטים
- ✅ מערכת שעובדת ומוכנה להורדות נוספות
- ✅ נתונים מאורגנים לפי תיקיות
- ✅ כלים לניתוח והמשך הורדה

**הצעדים הבאים:**
1. סקור את התמונות שהורדת ב-`downloads/`
2. החלט אם אתה רוצה להוריד עוד
3. השתמש באופציות למעלה להמשך

**בהצלחה!** 🚀
