# Image Support Setup Guide

## Overview
The resume analyzer now supports **JPEG, PNG, and JPG image files** in addition to PDF and DOCX formats. This uses Tesseract OCR to extract text from images.

## Supported File Formats
✅ PDF (.pdf)  
✅ DOCX (.docx)  
✅ **NEW: JPEG (.jpeg)**  
✅ **NEW: JPG (.jpg)**  
✅ **NEW: PNG (.png)**  

## Backend Changes

### 1. New Dependencies Installed
```bash
pytesseract==0.3.13  # Python OCR wrapper
pillow==11.3.0       # Image processing library
```

### 2. Code Updates
- **Updated**: `backend/analyzer/utils.py`
  - Added image file support with OCR
  - Added error handling with helpful messages
  - Supports JPEG, PNG, JPG formats

- **Updated**: `backend/analyzer/views.py`
  - No changes needed (automatic support)

### 3. Frontend Updates
- **Updated**: `frontend/src/App.jsx`
  - Updated file input to accept image formats
  - Updated description text

## Installation Steps

### Step 1: Install Python Libraries
Python packages are already installed via pip:
```bash
pip install pytesseract pillow
```

### Step 2: Install Tesseract OCR Engine

#### For Windows:
1. Download the Tesseract installer from:
   - **URL**: https://github.com/UB-Mannheim/tesseract/wiki
   - Look for "Downloads" section
   - Download the latest **tesseract-ocr-w64-setup-v5.x.x.exe**

2. Run the installer:
   - Execute the `.exe` file
   - Accept default settings (or note custom installation path)
   - Default installs to: `C:\Program Files\Tesseract-OCR`

3. Verify installation:
   ```bash
   tesseract --version
   ```
   Should output version info

#### For macOS:
```bash
brew install tesseract
```

#### For Linux (Ubuntu/Debian):
```bash
sudo apt-get install tesseract-ocr
```

### Step 3: Configure Path (Windows Only)

If Tesseract is installed in a non-standard location, update the path in `backend/analyzer/utils.py`:

```python
# Line 16 in utils.py - adjust this path to your installation
pytesseract.pytesseract_cmd = r'C:\Path\To\Tesseract-OCR\tesseract.exe'
```

Common locations:
- `C:\Program Files\Tesseract-OCR\tesseract.exe`
- `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`

## How It Works

### Upload Flow
```
1. User uploads image (JPEG, PNG, JPG)
   ↓
2. Backend receives file
   ↓
3. Image is loaded using Pillow
   ↓
4. Tesseract OCR extracts text from image
   ↓
5. Text is analyzed for career fields
   ↓
6. Results displayed to user
```

### OCR Process
- **Image Optimization**: Converts image to RGB for better OCR accuracy
- **Text Extraction**: Tesseract reads text from image
- **Validation**: Checks if text was successfully extracted
- **Error Handling**: Provides helpful error messages if OCR fails

## Error Messages & Solutions

### "Tesseract OCR is not installed"
**Solution**: Install Tesseract OCR from the link above

### "No text detected in image"
**Possible causes**:
- Image is too small or blurry
- Image doesn't contain readable text
- Image quality is poor

**Solutions**:
- Use a clearer, higher-resolution image
- Ensure text in image is readable
- Try using PDF or DOCX instead

### "tesseract is not installed / TesseractNotFoundError"
**Solution**: 
- Verify Tesseract is installed: `tesseract --version`
- Check installation path matches code
- Restart backend server after installation

## Testing Image Support

### Test with a Screenshot
1. Take a screenshot of your resume or a document
2. Save it as PNG or JPG
3. Upload to the resume analyzer
4. Verify text is extracted and analyzed

### Test with Multiple Images
Try different image types:
- Screenshots (PNG)
- Photos of documents (JPG/JPEG)
- Scanned documents (PNG/JPG)

## Performance Considerations

### Image Processing Time
- **Typical processing**: 2-5 seconds per image
- **Large images**: May take longer
- **Complex text**: May take longer

### Image Size Recommendations
- **Min**: 200x300 pixels (readable)
- **Optimal**: 600x900 pixels (professional document)
- **Max**: No hard limit, but very large images slow processing

### Quality Tips
- Use high-resolution images (300+ DPI preferred)
- Ensure good lighting and contrast
- Avoid rotated or skewed images
- Clean, readable text works best

## Troubleshooting

### Issue: Backend crashes on image upload
**Check**:
1. Tesseract is installed: `tesseract --version`
2. Tesseract path is correct in utils.py
3. Backend logs for specific error message

### Issue: Text extraction is incomplete or inaccurate
**Try**:
1. Use higher resolution image
2. Ensure image is properly oriented
3. Try a different image format
4. Use PDF or DOCX for better accuracy

### Issue: Very slow image processing
**Check**:
1. Image file size (very large images slow down processing)
2. System RAM availability
3. CPU usage
**Solution**: Use smaller images or wait longer

## API Response for Images

When an image is uploaded, the response includes:
```json
{
  "message": "Resume analyzed successfully using AI",
  "resume_id": 1,
  "ai_result": { ... },
  "field_analysis": { ... },
  "extracted_text": "Text extracted from image via OCR..."
}
```

The `extracted_text` will contain all text found by Tesseract OCR.

## Best Practices

✅ **DO**:
- Use clear, readable images
- Ensure proper lighting
- Keep documents flat/straight
- Use high resolution images
- Test with small images first

❌ **DON'T**:
- Use blurry images
- Use extremely large files (slow processing)
- Upload rotated/skewed images
- Use images with very small text
- Expect perfect accuracy with poor quality images

## Advanced Configuration

### Tesseract Languages
By default, Tesseract uses English. To support other languages:

```python
# In utils.py, modify the OCR call:
text = pytesseract.image_to_string(image, lang='eng')  # English
text = pytesseract.image_to_string(image, lang='fra')  # French
text = pytesseract.image_to_string(image, lang='eng+fra')  # English + French
```

Available languages: https://github.com/UltimateHackers/Tesseract-languages

### Image Preprocessing (Advanced)
For problematic images, enhance them before OCR:

```python
import cv2
import numpy as np

# Grayscale
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Threshold (binary)
_, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

# Denoise
image = cv2.fastNlMeansDenoising(image)
```

## Future Enhancements

Potential improvements:
- [ ] Batch image processing
- [ ] Multi-language support
- [ ] Image preprocessing for better accuracy
- [ ] PDF image page support
- [ ] Document orientation auto-correction
- [ ] Handwriting recognition

## Support

For issues:
1. Check the troubleshooting section above
2. Verify Tesseract installation
3. Check backend logs for error details
4. Try with a different image file

---

**Summary**: Image support is now fully integrated! Users can upload resume images (JPEG/PNG/JPG) and the OCR system will extract text for analysis. Install Tesseract OCR to enable this feature.
