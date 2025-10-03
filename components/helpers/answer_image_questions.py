import io
from google.cloud import vision
from openai import OpenAI

vision_client = vision.ImageAnnotatorClient()
openai_client = OpenAI()


def extract_question_from_image(image_path: str) -> str:

    try:
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = vision_client.document_text_detection(image=image)

        if response.error.message:
            print("Vision API error:", response.error.message)
        else:
            extracted_text = response.full_text_annotation.text.strip()
            if extracted_text:
                print("OCR Extracted Text (Vision):", extracted_text)
                return extracted_text
    except Exception as e:
        print("Vision OCR failed:", e)
