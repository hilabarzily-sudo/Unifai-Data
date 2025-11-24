# 🗂️ מדריך להורדה מקוטלגת של Civitai

## 📋 סיכום

סקריפט **`download_categorized.py`** מוריד את כל התוכן מ-Civitai מאורגן לפי סוג המודל (LORA, Checkpoint, וכו').

---

## 🎯 מה מוריד הסקריפט?

### תוכן מלא לכל מודל:
- 📸 **תמונות** (JPG, PNG, WebP)
- 🎬 **וידאו** (MP4, WebM)
- 📝 **פרומפטים** עם מטאדטה מלאה
- 📄 **תיאורי מודל** (articles)

### מאורגן לפי 9 קטגוריות:
```
unifai_data_catch/
├── LORA/                 (1,706 מודלים - 85.3%)
├── Checkpoint/           (205 מודלים - 10.2%)
├── Workflows/            (37 מודלים)
├── LoCon/                (34 מודלים)
├── TextualInversion/     (5 מודלים)
├── DoRA/                 (5 מודלים)
├── Wildcards/            (4 מודלים)
├── VAE/                  (1 מודל)
└── Other/                (3 מודלים)
```

**סה"כ:** 2,000 מודלים מקוטלגים!

---

## 🚀 איך להפעיל?

### 1️⃣ הורדה מלאה של הכל (2,000 מודלים)

```bash
cd /home/user/Unifai-Data/civitai-scraper
python3 download_categorized.py --max-items 30
```

**פרמטרים:**
- `--max-items 30` - עד 30 תמונות/וידאו לכל מודל

**זמן משוער:** ~10-15 שעות (תלוי במהירות אינטרנט)

---

### 2️⃣ הורדת קטגוריות ספציפיות

#### רק LORA (1,706 מודלים):
```bash
python3 download_categorized.py --categories LORA --max-items 30
```

#### רק Checkpoints (205 מודלים):
```bash
python3 download_categorized.py --categories Checkpoint --max-items 30
```

#### מספר קטגוריות:
```bash
python3 download_categorized.py --categories LORA Checkpoint Workflows --max-items 30
```

---

### 3️⃣ בדיקה מהירה (5 מודלים לקטגוריה)

```bash
python3 download_categorized.py --test --max-items 5
```

**טוב לפני:** הורדה מלאה, כדי לוודא שהכל עובד

---

### 4️⃣ אופציות מתקדמות

#### הורדה עם פחות תמונות למודל:
```bash
python3 download_categorized.py --max-items 10
```

#### שינוי תיקיית פלט:
```bash
python3 download_categorized.py --output /path/to/custom/dir --max-items 30
```

#### עזרה:
```bash
python3 download_categorized.py --help
```

---

## 📊 מה יקרה במהלך ההורדה?

### דוגמה לפלט:
```
======================================================================
🚀 CIVITAI CATEGORIZED DOWNLOADER
======================================================================
CSV File: outputs/civitai_fixed_20251124_161134.csv
Output Root: ./unifai_data_catch
Max items per model: 30
======================================================================

📂 LOADING MODELS FROM CSV
======================================================================

📊 Models by Category:
----------------------------------------------------------------------
  LORA                :  1706 models
  Checkpoint          :   205 models
  Workflows           :    37 models
  LoCon               :    34 models
  ...
----------------------------------------------------------------------
  TOTAL               :  2000 models

📁 Creating category directories...
  ✓ LORA/
  ✓ Checkpoint/
  ...

======================================================================
📥 DOWNLOADING: LORA
======================================================================
Models to process: 1706
Max items per model: 30
Output: unifai_data_catch/LORA
======================================================================

📦 LORA: 100%|██████████| 1706/1706 [02:15:30<00:00, 12.5s/model]

----------------------------------------------------------------------
📊 LORA Statistics:
  Models processed: 1706
  Images downloaded: 48,523
  Videos downloaded: 342
  Prompts saved: 48,865
  Errors: 12
----------------------------------------------------------------------
```

---

## 📁 מבנה התיקיות שייווצר

```
unifai_data_catch/
│
├── LORA/
│   ├── Styles For Pony Diffusion V6 XL/
│   │   ├── images/
│   │   │   ├── image_001_0.jpg
│   │   │   ├── image_002_1.jpg
│   │   │   └── ...
│   │   ├── videos/
│   │   │   └── video_001_0.mp4
│   │   ├── prompts/
│   │   │   ├── image_001_0_prompt.txt
│   │   │   ├── image_001_0_metadata.json
│   │   │   └── ...
│   │   ├── articles/
│   │   │   └── model_description.txt
│   │   └── model_info.json
│   │
│   ├── CAT - Citron Styles/
│   │   └── (same structure)
│   │
│   └── ...
│
├── Checkpoint/
│   ├── CyberRealistic Pony/
│   ├── PerfectDeliberate/
│   └── ...
│
├── Workflows/
│   └── ...
│
└── (other categories...)
```

כל מודל מאורגן בתיקייה נפרדת עם כל התוכן שלו!

---

## 📈 תוצאות צפויות

### הערכת גודל (עבור הורדה מלאה):

| קטגוריה | מודלים | תמונות משוערות | גודל משוער |
|---------|--------|----------------|------------|
| LORA | 1,706 | ~51,000 | ~150-200 GB |
| Checkpoint | 205 | ~6,000 | ~20-30 GB |
| Workflows | 37 | ~1,100 | ~3-5 GB |
| אחרים | 52 | ~1,600 | ~5-10 GB |
| **סה"כ** | **2,000** | **~60,000** | **~200-250 GB** |

**הערה:** גודל בפועל תלוי ב:
- איכות התמונות
- כמות וידאו (קבצים גדולים מאוד!)
- `--max-items` שבחרת

---

## ⚡ טיפים לאופטימיזציה

### 1. הורדה מקבילית של קטגוריות

אפשר להריץ מספר הורדות במקביל בטרמינלים שונים:

```bash
# Terminal 1
python3 download_categorized.py --categories LORA --max-items 30

# Terminal 2
python3 download_categorized.py --categories Checkpoint --max-items 30

# Terminal 3
python3 download_categorized.py --categories Workflows --max-items 30
```

### 2. הורדה בשלבים

התחל עם `--max-items 10` ואז הגדל ל-30 בריצה שנייה.

### 3. ניטור התקדמות

כל קטגוריה שומרת סטטיסטיקות ב:
```
unifai_data_catch/LORA/lora_stats.json
unifai_data_catch/Checkpoint/checkpoint_stats.json
...
```

---

## 🛑 עצירה והמשך

### לעצור באמצע:
```
Ctrl+C
```

### להמשיך מאותו מקום:
הסקריפט **לא מוריד** קבצים שכבר קיימים, אז פשוט תריץ שוב את אותה פקודה.

---

## 🔍 בדיקת התוצאות

### 1. ספירת קבצים שהורדו:

```bash
# כל התמונות
find unifai_data_catch/ -name "*.jpg" -o -name "*.png" | wc -l

# כל הווידאו
find unifai_data_catch/ -name "*.mp4" -o -name "*.webm" | wc -l

# כל הפרומפטים
find unifai_data_catch/ -name "*_prompt.txt" | wc -l
```

### 2. גודל כולל:

```bash
du -sh unifai_data_catch/
```

### 3. גודל לפי קטגוריה:

```bash
du -sh unifai_data_catch/*/
```

---

## 📦 העברה ל-Windows

### אופציה 1: העתקה ישירה (WSL)

```bash
# אם יש לך גישה ישירה ל-D:
cp -r unifai_data_catch /mnt/d/unifai_data_catch
```

### אופציה 2: ארכיון ו-transfer

```bash
# יצירת ארכיון (דחוס)
tar -czf unifai_data.tar.gz unifai_data_catch/

# העתק ל-Windows
cp unifai_data.tar.gz /mnt/c/Users/YourName/Downloads/
```

אחר כך ב-Windows:
1. פתח את הארכיון ב-7-Zip / WinRAR
2. חלץ ל-`D:\unifai_data_catch\`

### אופציה 3: SCP/FTP

ראה [WINDOWS_TRANSFER_GUIDE.md](./WINDOWS_TRANSFER_GUIDE.md) למידע מלא.

---

## 🐛 פתרון בעיות

### בעיה 1: "No module named 'pandas'"
```bash
pip install pandas tqdm requests openpyxl
```

### בעיה 2: "Permission denied"
```bash
chmod +x download_categorized.py
```

### בעיה 3: "Disk space full"
בדוק שיש לך לפחות 300 GB פנויים:
```bash
df -h
```

### בעיה 4: "Connection timeout"
הסקריפט ינסה שוב אוטומטית. אם הבעיה נמשכת, בדוק חיבור אינטרנט.

### בעיה 5: "Rate limit exceeded"
הסקריפט כבר כולל rate limiting (0.3s delay). אם עדיין יש בעיה, הגדל את ה-delay ב-`config.py`:
```python
API_CONFIG = {
    "rate_limit_delay": 1.0,  # Change from 0.5 to 1.0
}
```

---

## 📊 סטטיסטיקות בזמן אמת

במהלך ההורדה, תראה:

```
📦 LORA:  45%|████▌     | 768/1706 [01:32:15<01:45:22, 11.8s/model]
```

- **45%** - התקדמות באחוזים
- **768/1706** - מודלים שהורדו / סה"כ
- **01:32:15** - זמן שעבר
- **01:45:22** - זמן משוער שנותר
- **11.8s/model** - ממוצע זמן למודל

---

## ✅ בדיקת שלמות

### בדיקה אם כל המודלים הורדו:

```bash
# הצג מודלים שלא הורדו (תיקיות ריקות)
find unifai_data_catch/ -type d -empty
```

### בדיקה אם יש שגיאות:

```bash
# בדוק את קבצי הסטטיסטיקות
cat unifai_data_catch/*/stats.json | grep errors
```

---

## 🎉 סיכום מהיר

### הפקודה הכי פשוטה - הורדת הכל:

```bash
python3 download_categorized.py --max-items 30
```

**זהו!** הסקריפט יעשה הכל עבורך:
1. ✅ יטען את רשימת המודלים מה-CSV
2. ✅ יצור תיקיות לפי קטגוריות
3. ✅ יוריד תמונות, וידאו, ופרומפטים לכל מודל
4. ✅ יארגן הכל בתיקיות נפרדות
5. ✅ ישמור סטטיסטיקות מפורטות

---

## 📞 תמיכה

- **תיעוד מפורט:** [README.md](./README.md)
- **מדריך שימוש:** [USAGE_GUIDE.md](./USAGE_GUIDE.md)
- **מדריך הורדה:** [DOWNLOAD_GUIDE.md](./DOWNLOAD_GUIDE.md)
- **אימות מימוש:** [IMPLEMENTATION_VALIDATION.md](./IMPLEMENTATION_VALIDATION.md)

---

**🎊 בהצלחה עם ההורדה!**

כל התוכן יהיה מאורגן מושלם ב-`unifai_data_catch/` מוכן להעברה ל-`D:\unifai_data_catch` 🚀
