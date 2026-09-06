
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit.processor import IndicProcessor


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

SRC_LANG = "hin_Deva"
TGT_LANG = "eng_Latn"

MODEL_NAME = "ai4bharat/indictrans2-indic-en-dist-200M"


print(f"Loading IndicTrans2 200M on {DEVICE}...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    dtype=torch.float16 if DEVICE == "cuda" else torch.float32
).to(DEVICE)

ip = IndicProcessor(inference=True)

print("IndicTrans2 200M loaded successfully!")


def translate_hindi(text):
    if not text or not text.strip():
        return ""

    input_sentences = [text.strip()]

    batch = ip.preprocess_batch(
        input_sentences,
        src_lang=SRC_LANG,
        tgt_lang=TGT_LANG
    )

    encodings = tokenizer(
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
        generated_tokens = model.generate(
            **encodings,
            num_beams=1,
            do_sample=False,
            max_length=256,
            use_cache=False
        )

    decoded = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    translations = ip.postprocess_batch(
        decoded,
        lang=TGT_LANG
    )

    return translations[0]
