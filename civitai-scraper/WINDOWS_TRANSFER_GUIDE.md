# העברה ל-Windows: D:\unifai_data_catch

## 📍 איפה הכל נמצא עכשיו:

```
/home/user/Unifai-Data/civitai-scraper/
```

## 🎯 לאן להעביר:

```
D:\unifai_data_catch\
```

---

## 🚀 שלב 1: הורד את כל התוכן

### אופציה A: 100 מודלים (מומלץ להתחלה)
```bash
cd /home/user/Unifai-Data/civitai-scraper
python download_everything.py
```

זה יוריד ל:
- `./unifai_data_catch/` (מוכן להעברה)
- זמן: ~30-40 דקות
- גודל: ~5-8 GB

### אופציה B: כל 2,000 המודלים
ערוך את `download_everything.py`:
```python
max_models = 2000  # במקום 100
max_items_per_model = 30
```

ואז:
```bash
python download_everything.py
```

זמן: ~10-15 שעות
גודל: ~80-100 GB

---

## 🔄 שלב 2: העברה ל-Windows

### **Method 1: Windows Subsystem for Linux (WSL) - הכי קל!**

אם אתה ב-WSL, הכונן D:\ כבר נגיש:

```bash
# צור תיקייה ב-D:
mkdir -p /mnt/d/unifai_data_catch

# העתק הכל
cp -r unifai_data_catch/* /mnt/d/unifai_data_catch/

# בדוק שהועתק
ls -lh /mnt/d/unifai_data_catch/
```

זהו! עכשיו יש לך הכל ב-`D:\unifai_data_catch\`

---

### **Method 2: SCP/SFTP (מ-Linux מרוחק ל-Windows)**

אם אתה ב-Linux server ורוצה להעביר ל-Windows:

```bash
# דחוס את הכל (מהיר יותר להעברה)
tar -czf unifai_data.tar.gz unifai_data_catch/

# או zip
zip -r unifai_data.zip unifai_data_catch/

# העבר ל-Windows (WinSCP או SFTP)
# או:
scp unifai_data.tar.gz your-user@windows-ip:D:/
```

אז ב-Windows:
1. חלץ את הקובץ
2. העבר את התיקייה `unifai_data_catch` ל-`D:\`

---

### **Method 3: Shared Folder (VirtualBox/VMware)**

אם אתה ב-VM:

1. הגדר Shared Folder ב-VM settings
2. Mount ה-shared folder:
```bash
mkdir -p /mnt/shared
mount -t vboxsf ShareName /mnt/shared

# העתק
cp -r unifai_data_catch /mnt/shared/
```

---

### **Method 4: Cloud Storage (גדול מדי? העלה לענן)**

```bash
# Google Drive (עם rclone)
rclone copy unifai_data_catch gdrive:unifai_data_catch

# או Dropbox
rclone copy unifai_data_catch dropbox:unifai_data_catch

# אז הורד מהענן ל-Windows
```

---

## 📁 מבנה הסופי ב-Windows

אחרי ההעברה, ב-`D:\unifai_data_catch\` יהיה:

```
D:\unifai_data_catch\
├── CyberRealistic Pony\
│   ├── images\
│   │   ├── image_001_0.jpg
│   │   ├── image_002_1.jpg
│   │   └── ... (עד 30 תמונות)
│   ├── videos\
│   │   ├── video_001_0.mp4
│   │   └── ... (וידאו אם יש)
│   ├── prompts\
│   │   ├── image_001_0_prompt.txt      ← הפרומפט!
│   │   ├── image_001_0_metadata.json   ← המטאדטה
│   │   └── ...
│   ├── articles\
│   │   └── model_description.txt       ← המאמר/תיאור
│   └── model_info.json                 ← מידע כללי
├── Nova Anime XL\
├── PerfectDeliberate\
└── ... (עוד 97-1997 מודלים)
```

---

## 📊 מה כלול בכל תיקייה:

### 📸 images/
- כל התמונות מהמודל
- פורמטים: JPG, PNG, WebP
- באיכות מלאה

### 🎬 videos/
- כל הסרטונים מהמודל (אם יש)
- פורמטים: MP4, WebM
- באיכות מלאה

### 📝 prompts/
- לכל תמונה/וידאו:
  - `*_prompt.txt` - הפרומפט הקריא
  - `*_metadata.json` - כל ההגדרות (steps, sampler, CFG, seed...)

### 📄 articles/
- `model_description.txt` - התיאור המלא של המודל

### 📋 model_info.json
- שם המודל
- קישור לאתר
- יוצר
- סוג (Checkpoint, LORA, etc.)
- Base model (Illustrious, Flux, etc.)
- כמות הורדות
- תגיות

---

## 🔍 איך לגשת לפרומפטים ב-Windows:

### שיטה 1: פתח קובץ ישירות
```
D:\unifai_data_catch\CyberRealistic Pony\prompts\image_001_0_prompt.txt
```

### שיטה 2: קרא את כל הפרומפטים ב-Python
```python
import os
import json

# קרא מידע מודל
with open(r'D:\unifai_data_catch\CyberRealistic Pony\model_info.json', 'r') as f:
    model_info = json.load(f)
    print(f"Model: {model_info['model_name']}")
    print(f"Type: {model_info['type']}")

# קרא פרומפט
with open(r'D:\unifai_data_catch\CyberRealistic Pony\prompts\image_001_0_prompt.txt', 'r') as f:
    prompt = f.read()
    print(f"\nPrompt:\n{prompt}")
```

### שיטה 3: חיפוש פרומפטים
```batch
:: ב-Windows CMD - חפש פרומפטים שמכילים מילה מסוימת
cd D:\unifai_data_catch
findstr /s /i "masterpiece" *_prompt.txt
```

או ב-PowerShell:
```powershell
# מצא את כל הפרומפטים
Get-ChildItem -Recurse -Filter "*_prompt.txt" | Select-Object FullName

# מצא פרומפטים שמכילים "portrait"
Get-ChildItem -Recurse -Filter "*_prompt.txt" | Select-String "portrait"
```

---

## 📈 סטטיסטיקות צפויות:

### 100 מודלים:
- תמונות: ~1,000-3,000
- וידאו: ~50-150
- פרומפטים: ~1,000-3,000
- גודל: 5-8 GB
- זמן הורדה: 30-40 דקות

### 2,000 מודלים:
- תמונות: ~20,000-60,000
- וידאו: ~1,000-3,000
- פרומפטים: ~20,000-60,000
- גודל: 80-120 GB
- זמן הורדה: 10-15 שעות

---

## ⚡ טיפים לביצועים:

### 1. העברה מהירה יותר
```bash
# דחוס לפני העברה (חוסך זמן ברשת)
tar -czf unifai.tar.gz unifai_data_catch/

# או עם pigz (מקבילי - מהיר יותר)
tar -I pigz -cf unifai.tar.gz unifai_data_catch/
```

### 2. בדוק שלמות
```bash
# ספור קבצים לפני
find unifai_data_catch -type f | wc -l

# אחרי העברה ב-Windows (PowerShell):
(Get-ChildItem -Path "D:\unifai_data_catch" -Recurse -File).Count
```

### 3. מהירות קריאה ב-Windows
- אחסן ב-SSD (לא HDD) לביצועים
- השתמש ב-Windows Search indexing
- או SQLite database לחיפוש מהיר

---

## 🛠️ פתרון בעיות:

### "אין מספיק מקום ב-D:\"
```bash
# בדוק כמה מקום יש
df -h  # בLinux

# ב-Windows:
# לחץ ימני על D:\ → Properties
```

פתרונות:
1. נקה מקום ב-D:\
2. העבר לכונן אחר (E:\, F:\...)
3. דחוס חלק מהתמונות
4. הורד פחות מודלים (max_models=50)

### "ההעברה איטית מדי"
1. דחוס לפני העברה
2. העבר בלילה
3. השתמש ב-LAN cable (לא WiFi)

### "הקבצים לא נפתחים ב-Windows"
- ודא encoding: UTF-8
- פתח עם Notepad++ או VS Code (לא Notepad)

---

## 🎓 דוגמאות שימוש ב-Windows:

### Python Script - מצא את 10 הפרומפטים הטובים ביותר
```python
import os
import json
from pathlib import Path

base = Path(r"D:\unifai_data_catch")

prompts_with_quality = []

# סרוק את כל המודלים
for model_dir in base.iterdir():
    if not model_dir.is_dir():
        continue

    # קרא model info
    info_file = model_dir / "model_info.json"
    if info_file.exists():
        with open(info_file, 'r', encoding='utf-8') as f:
            model_info = json.load(f)

        # קרא פרומפטים
        prompts_dir = model_dir / "prompts"
        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob("*_prompt.txt"):
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompt = f.read()
                    if len(prompt) > 100:  # רק פרומפטים עם תוכן
                        prompts_with_quality.append({
                            'model': model_info['model_name'],
                            'downloads': model_info['downloads'],
                            'prompt': prompt,
                            'file': str(prompt_file)
                        })

# מיין לפי downloads
prompts_with_quality.sort(key=lambda x: x['downloads'], reverse=True)

# הצג את 10 הטובים
for i, item in enumerate(prompts_with_quality[:10], 1):
    print(f"\n{i}. {item['model']} ({item['downloads']:,} downloads)")
    print(f"Prompt: {item['prompt'][:200]}...")
```

---

## ✅ צ'קליסט

- [ ] הורדתי את כל התוכן (`python download_everything.py`)
- [ ] בדקתי את הגודל (`du -sh unifai_data_catch`)
- [ ] דחסתי אם צריך (`tar -czf unifai.tar.gz unifai_data_catch/`)
- [ ] העברתי ל-Windows D:\
- [ ] אימתתי שכל הקבצים הועתקו
- [ ] בדקתי שאני יכול לפתוח פרומפטים
- [ ] יצרתי backup!

---

## 🎉 זהו!

עכשיו יש לך:
- ✅ אלפי תמונות עם פרומפטים
- ✅ מאות וידאו עם פרומפטים
- ✅ מאמרים ותיאורים
- ✅ כל המטאדטה (steps, sampler, CFG, seed...)
- ✅ מאורגן בתיקיות לפי מודל

**כל מה שצריך לאימון AI ולמחקר!** 🚀

---

## 📞 עזרה נוספת

אם יש בעיות, בדוק:
1. `README.md` - תיעוד מלא
2. `DOWNLOAD_GUIDE.md` - מדריך הורדה
3. `USAGE_GUIDE.md` - שימוש כללי

**בהצלחה!** 💪
