
# HindiLens API Contract

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
  "english_text": "beware",
  "error": null
}
