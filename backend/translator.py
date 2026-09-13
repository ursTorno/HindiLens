
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor
from huggingface_hub import snapshot_download


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ============================================================
# 1. HINDI → ENGLISH
# ============================================================

MODEL_NAME_HI_EN = "ai4bharat/indictrans2-indic-en-dist-200M"

LOCAL_MODEL_PATH_HI_EN = snapshot_download(
    repo_id=MODEL_NAME_HI_EN
)

tokenizer_hi_en = AutoTokenizer.from_pretrained(
    LOCAL_MODEL_PATH_HI_EN,
    trust_remote_code=True,
    local_files_only=True
)

model_hi_en = AutoModelForSeq2SeqLM.from_pretrained(
    LOCAL_MODEL_PATH_HI_EN,
    trust_remote_code=True,
    local_files_only=True,
    dtype=torch.float16 if DEVICE == "cuda" else torch.float32
).to(DEVICE)

ip_hi_en = IndicProcessor(inference=True)


def translate_hindi(text):
    if not text or not text.strip():
        return ""

    batch = ip_hi_en.preprocess_batch(
        [text.strip()],
        src_lang="hin_Deva",
        tgt_lang="eng_Latn"
    )

    encodings = tokenizer_hi_en(
        batch,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=256
    )

    encodings = {
        key: value.to(DEVICE)
        for key, value in encodings.items()
    }

    with torch.inference_mode():
        generated_tokens = model_hi_en.generate(
            **encodings,
            num_beams=5,
            max_length=256,
            use_cache=False
        )

    decoded = tokenizer_hi_en.batch_decode(
        generated_tokens,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    translations = ip_hi_en.postprocess_batch(
        decoded,
        lang="eng_Latn"
    )

    return translations[0]


# ============================================================
# 2. ENGLISH → HINDI
# ============================================================

MODEL_NAME_EN_HI = "ai4bharat/indictrans2-en-indic-dist-200M"

LOCAL_MODEL_PATH_EN_HI = snapshot_download(
    repo_id=MODEL_NAME_EN_HI
)

tokenizer_en_hi = AutoTokenizer.from_pretrained(
    LOCAL_MODEL_PATH_EN_HI,
    trust_remote_code=True,
    local_files_only=True
)

model_en_hi = AutoModelForSeq2SeqLM.from_pretrained(
    LOCAL_MODEL_PATH_EN_HI,
    trust_remote_code=True,
    local_files_only=True,
    dtype=torch.float16 if DEVICE == "cuda" else torch.float32
).to(DEVICE)

ip_en_hi = IndicProcessor(inference=True)


def translate_english_to_hindi(text):
    if not text or not text.strip():
        return ""

    batch = ip_en_hi.preprocess_batch(
        [text.strip()],
        src_lang="eng_Latn",
        tgt_lang="hin_Deva"
    )

    encodings = tokenizer_en_hi(
        batch,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=256
    )

    encodings = {
        key: value.to(DEVICE)
        for key, value in encodings.items()
    }

    with torch.inference_mode():
        generated_tokens = model_en_hi.generate(
            **encodings,
            num_beams=5,
            max_length=256,
            use_cache=False
        )

    decoded = tokenizer_en_hi.batch_decode(
        generated_tokens,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    translations = ip_en_hi.postprocess_batch(
        decoded,
        lang="hin_Deva"
    )

    return translations[0]
