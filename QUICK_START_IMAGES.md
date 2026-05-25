# Quick Start - Image Support

## ✅ What's Ready

Your resume analyzer now supports **image uploads** (JPEG, PNG, JPG)!

## ⏳ What You Need to Do

### 1 Minute Setup - Install Tesseract OCR

**Windows Users**:
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Look for "Downloads" section
3. Download: `tesseract-ocr-w64-setup-v5.x.x.exe`
4. Run installer (accept defaults)
5. Done! ✅

**macOS**:
```bash
brew install tesseract
```

**Linux**:
```bash
sudo apt-get install tesseract-ocr
```

### Verify Installation

Open terminal/command prompt and run:
```bash
tesseract --version
```

Should show version info. ✅

## 🚀 Ready to Test

```bash
# Terminal 1 - Backend
cd c:\resume_analyzer\backend
python manage.py runserver

# Terminal 2 - Frontend
cd c:\resume_analyzer\frontend
npm run dev
```

Visit: http://localhost:5173

## 📸 Try It Out

1. **Take a screenshot** of your resume or document
2. **Save as PNG or JPG**
3. **Upload to the app**
4. **Wait 2-5 seconds** for OCR processing
5. **View results** - same analysis as PDF/DOCX!

## 📋 Supported Formats

✅ PDF  
✅ DOCX  
✅ **JPEG** ← NEW  
✅ **PNG** ← NEW  
✅ **JPG** ← NEW  

## 🎯 What Happens

```
Image Upload
    ↓
OCR extracts text
    ↓
AI analyzes for all 10 fields
    ↓
Show scores & recommendations
```

## 🆘 Issues?

**"Tesseract not installed"**
→ Run installer from GitHub link above

**"No text detected in image"**
→ Use clearer, higher-resolution image

**"Text extraction incomplete"**
→ Try PDF/DOCX format instead

---

**That's it!** Install Tesseract and you're all set to use image files! 🎉
