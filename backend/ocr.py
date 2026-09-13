
import re
import cv2
import pytesseract


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


def contains_hindi_letters(text):
    return bool(
        re.search(
            r'[\u0905-\u0939\u0958-\u095F]',
            text
        )
    )


def ocr_hindi(image_path, confidence_threshold=70):
    processed = preprocess_image(image_path)

    candidates = []

    for psm in [6, 7, 11]:

        data = pytesseract.image_to_data(
            processed,
            lang="hin",
            config=f"--psm {psm}",
            output_type=pytesseract.Output.DICT
        )

        words = []
        confidences = []

        for i in range(len(data["text"])):
            text = data["text"][i].strip()

            if not text:
                continue

            try:
                confidence = float(data["conf"][i])
            except:
                continue

            if confidence >= confidence_threshold:
                words.append(text)
                confidences.append(confidence)

        if not words:
            continue

        candidate_text = " ".join(words)

        if not contains_hindi_letters(candidate_text):
            continue

        average_confidence = sum(confidences) / len(confidences)

        candidates.append({
            "psm": psm,
            "text": candidate_text,
            "confidence": average_confidence,
            "word_count": len(words)
        })

    if not candidates:
        return ""

    best = max(
        candidates,
        key=lambda x: (x["word_count"], x["confidence"])
    )

    return best["text"]


def ocr_english(image_path, confidence_threshold=50):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Enlarge image
    gray = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # Reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Create thresholded version
    _, thresh = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    candidates = []

    # Try both preprocessing versions
    for processed in [gray, thresh]:

        # Try different page segmentation modes
        for psm in [6, 7, 11]:

            data = pytesseract.image_to_data(
                processed,
                lang="eng",
                config=f"--psm {psm}",
                output_type=pytesseract.Output.DICT
            )

            words = []
            confidences = []

            for i in range(len(data["text"])):
                text = data["text"][i].strip()

                if not text:
                    continue

                try:
                    confidence = float(data["conf"][i])
                except:
                    continue

                if confidence >= confidence_threshold:
                    words.append(text)
                    confidences.append(confidence)

            if not words:
                continue

            candidate_text = " ".join(words)

            average_confidence = (
                sum(confidences) / len(confidences)
            )

            candidates.append({
                "text": candidate_text,
                "confidence": average_confidence,
                "word_count": len(words)
            })

    if not candidates:
        return ""

    # Prefer more recognized words,
    # then use confidence as tie-breaker
    best = max(
        candidates,
        key=lambda x: (x["word_count"], x["confidence"])
    )

    return best["text"]
