
from fastapi import FastAPI, UploadFile, File
from backend.ocr import ocr_hindi
from backend.translator import translate_hindi
import tempfile
import os

app = FastAPI(title="HindiLens API")


@app.post("/translate")
async def translate_image(file: UploadFile = File(...)):

    temp_path = None

    try:
        # Save uploaded image temporarily
        suffix = os.path.splitext(file.filename or ".jpg")[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        # OCR
        hindi_text = ocr_hindi(temp_path)

        if not hindi_text:
            return {
                "hindi_text": "",
                "english_text": "",
                "error": "No readable Hindi text found"
            }

        # Translation
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
