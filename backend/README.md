
# HindiLens Backend

HindiLens is a mobile application that translates text between Hindi and English using OCR and machine translation.

## Current Backend Capabilities

The backend currently supports three operations:

1. Hindi image → English
2. English image → Hindi
3. English text → Hindi

---

## Architecture

```text
Hindi Image
    ↓
Hindi OCR (Tesseract)
    ↓
Hindi Text
    ↓
IndicTrans2
    ↓
English Text
