
# HindiLens Backend

This backend provides Hindi image-to-English translation.

## Pipeline

Image
→ Image preprocessing
→ Tesseract Hindi OCR
→ Hindi text
→ IndicTrans2
→ English translation
→ JSON response

## Files

- `ocr.py` — image preprocessing and Hindi OCR
- `translator.py` — IndicTrans2 Hindi-to-English translation
- `main.py` — FastAPI API

## API

### POST `/translate`

Upload a Hindi image using the field name:

`file`

Example response:

```json
{
    "hindi_text": "सावधान",
    "english_text": "beware",
    "error": null
}
