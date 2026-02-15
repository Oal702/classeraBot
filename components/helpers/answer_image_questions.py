import io
from google.cloud import vision

# GOOGLE CLOUD VISION OCR CONFIGURATION
# ============================================================================
# This bot ALWAYS compares images by their SRC on retry (second attempt).
#
# Enabling OCR below may improve first-attempt accuracy for image-based
# questions, but comes with trade-offs:
#   - PROS: Potentially higher scores on first try, fewer retries needed
#   - CONS: Slower performance, requires Google Cloud Vision setup
#
# If you encounter OCR errors or want faster performance, disable OCR by:
#   1. Commenting out the OCR-enabled version below
#   2. Uncommenting the OCR-disabled version at the bottom
# ============================================================================

# OCR ENABLED VERSION (uncomment to use)
# vision_client = vision.ImageAnnotatorClient()


# def extract_question_from_image(image_path: str) -> str:
#     """Extract text from image using Google Cloud Vision OCR."""
#     try:
#         with io.open(image_path, "rb") as image_file:
#             content = image_file.read()

#         image = vision.Image(content=content)
#         response = vision_client.document_text_detection(image=image)

#         if response.error.message:
#             print("Vision API error:", response.error.message)
#         else:
#             extracted_text = response.full_text_annotation.text.strip()
#             if extracted_text:
#                 print("OCR Extracted Text (Vision):", extracted_text)
#                 return extracted_text
#     except Exception as e:
#         print("Vision OCR failed:", e)

#     return ""


# ============================================================================
# OCR DISABLED VERSION (defualt)
# ============================================================================
# Use this if you want to skip OCR entirely and rely solely on SRC comparison.
# The bot will still work perfectly - it just won't attempt OCR on first try.
#
def extract_question_from_image(image_path: str) -> str:
    # Skip OCR and rely on SRC comparison (happens automatically on retry)
    return ""


# ============================================================================
