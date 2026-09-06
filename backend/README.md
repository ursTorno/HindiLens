# HindiLens Backend

This backend provides Hindi image-to-English translation using:

- Tesseract OCR with Hindi language data
- OpenCV image preprocessing
- IndicTrans2 for Hindi → English translation
- FastAPI for the REST API

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
- `test_backend.py` — backend functional tests
- `test_images/` — test images used by the backend tests
- `requirements.txt` — Python dependencies
- `API.md` — API contract and examples

## Requirements

- Python 3.10+
- Tesseract OCR
- Tesseract Hindi language data (`hin`)
- Internet connection for downloading the IndicTrans2 model
- Hugging Face account with access to the IndicTrans2 model
- CUDA GPU is recommended for practical inference

## 1. Install Python dependencies

From the project root:

    pip install -r backend/requirements.txt

## 2. Install Tesseract

On Ubuntu/Debian:

    sudo apt update
    sudo apt install -y tesseract-ocr tesseract-ocr-hin

Verify:

    tesseract --version
    tesseract --list-langs

The language list should include `hin`.

## 3. Hugging Face authentication

The backend loads:

    ai4bharat/indictrans2-indic-en-1B

The Hugging Face account running the backend must have access to this model.

Authenticate before starting the backend:

    huggingface-cli login

Enter a Hugging Face access token with read access.

Do not commit the token to GitHub.

## 4. Start the FastAPI server

From the project root:

    uvicorn backend.main:app --host 0.0.0.0 --port 8000

The API will be available at:

    http://localhost:8000

FastAPI documentation:

    http://localhost:8000/docs

## 5. Test the backend

From the project root:

    python backend/test_backend.py

Expected result:

    Result: 5/5 tests passed

## API

### POST `/translate`

Upload an image using the multipart/form-data field:

    file

Example successful response:

    {
        "hindi_text": "सावधान",
        "english_text": "beware",
        "error": null
    }

### No readable Hindi text

    {
        "hindi_text": "",
        "english_text": "",
        "error": "No readable Hindi text found"
    }

### Translation failure

If OCR succeeds but translation fails:

    {
        "hindi_text": "सावधान",
        "english_text": "",
        "error": "Translation failed: ..."
    }

### Image processing failure

If image processing fails:

    {
        "hindi_text": "",
        "english_text": "",
        "error": "Image processing failed: ..."
    }

See `API.md` for the complete API contract.

## Important deployment notes

`requirements.txt` does not install the Tesseract system package or Hindi language data.

The deployment machine must install:

- Tesseract OCR
- Tesseract Hindi language data (`hin`)

The deployment environment must also authenticate with Hugging Face so that IndicTrans2 can be loaded.

A CUDA-compatible GPU is recommended for practical inference performance.

## Project scope

The backend supports:

    Hindi image → Hindi OCR → Hindi text → IndicTrans2 → English translation

The first version supports Hindi → English only.
