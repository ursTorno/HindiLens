
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

test_images = [
    "hindi1.png",
    "hindi2.png",
    "hindi3.png",
    "hindi4.png",
    "hindi5.png",
]

print("HindiLens Backend Test")
print("=" * 60)

passed = 0

for image_path in test_images:

    try:
        with open(image_path, "rb") as image:
            response = client.post(
                "/translate",
                files={
                    "file": (
                        image_path,
                        image,
                        "image/png"
                    )
                }
            )

        result = response.json()

        if (
            response.status_code == 200
            and result["hindi_text"]
            and result["english_text"]
            and result["error"] is None
        ):
            print(f"PASS: {image_path}")
            passed += 1
        else:
            print(f"FAIL: {image_path}")
            print(result)

    except Exception as e:
        print(f"FAIL: {image_path}")
        print("Error:", e)

print("=" * 60)
print(f"Result: {passed}/{len(test_images)} tests passed")
