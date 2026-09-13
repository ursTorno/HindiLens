
from fastapi import FastAPI, UploadFile, File, Form

from backend.ocr import ocr_hindi, ocr_english
from backend.translator import (
    translate_hindi,
    translate_english_to_hindi
)

import tempfile
import os


app = FastAPI(title="HindiLens API")


# ============================================================
# 1. HINDI IMAGE → ENGLISH
# ============================================================

@app.post("/translate")
async def translate_hindi_image(file: UploadFile = File(...)):

    temp_path = None

    try:
        suffix = os.path.splitext(file.filename or ".jpg")[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(await file.read())
            temp_path = temp_file.name

        # Hindi OCR
        hindi_text = ocr_hindi(temp_path)

        if not hindi_text:
            return {
                "hindi_text": "",
                "english_text": "",
                "error": "No readable Hindi text found"
            }

        # Hindi → English
        try:
            english_text = translate_hindi(hindi_text)

            return {
                "hindi_text": hindi_text,
                "english_text": english_text,
                "error": None
            }

        except Exception as e:

            return {
                "hindi_text": hindi_text,
                "english_text": "",
                "error": f"Translation failed: {str(e)}"
            }

    except Exception as e:

        return {
            "hindi_text": "",
            "english_text": "",
            "error": f"Image processing failed: {str(e)}"
        }

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ============================================================
# 2. ENGLISH IMAGE → HINDI
# ============================================================

@app.post("/translate-en-hi")
async def translate_english_image(file: UploadFile = File(...)):

    temp_path = None

    try:
        suffix = os.path.splitext(file.filename or ".jpg")[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(await file.read())
            temp_path = temp_file.name

        # English OCR
        english_text = ocr_english(temp_path)

        if not english_text:
            return {
                "english_text": "",
                "hindi_text": "",
                "error": "No readable English text found"
            }

        # English → Hindi
        try:
            hindi_text = translate_english_to_hindi(english_text)

            return {
                "english_text": english_text,
                "hindi_text": hindi_text,
                "error": None
            }

        except Exception as e:

            return {
                "english_text": english_text,
                "hindi_text": "",
                "error": f"Translation failed: {str(e)}"
            }

    except Exception as e:

        return {
            "english_text": "",
            "hindi_text": "",
            "error": f"Image processing failed: {str(e)}"
        }

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ============================================================
# 3. ENGLISH TEXT → HINDI
# ============================================================

@app.post("/translate-text-en-hi")
async def translate_english_text(
    text: str = Form(...)
):

    if not text or not text.strip():

        return {
            "english_text": "",
            "hindi_text": "",
            "error": "English text is empty"
        }

    try:

        hindi_text = translate_english_to_hindi(text)

        return {
            "english_text": text,
            "hindi_text": hindi_text,
            "error": None
        }

    except Exception as e:

        return {
            "english_text": text,
            "hindi_text": "",
            "error": f"Translation failed: {str(e)}"
        }
