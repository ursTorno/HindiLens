
# HindiLens API Contract

The HindiLens backend supports three translation operations:

1. Hindi image → English
2. English image → Hindi
3. English text → Hindi


# 1. Hindi Image → English

## Endpoint

POST `/translate`

## Request

Send an image using `multipart/form-data`.

Field name:

`file`

## Successful Response

```json
{
  "hindi_text": "सावधान",
  "english_text": "Beware",
  "error": null
}
