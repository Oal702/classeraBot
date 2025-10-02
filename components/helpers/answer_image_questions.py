import base64
from openai import OpenAI

client = OpenAI()


def extract_question_from_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract the text from this image (Arabic + English). "
                    "Preserve original formatting as much as possible: "
                    "keep line breaks, spacing, indentation, symbols, arrows (⇒), and matrix layout. "
                    "Do not rephrase, translate, or add commentary. Output raw text only."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all visible text clearly:"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64_img}"},
                    },
                ],
            },
        ],
        temperature=0,
        max_completion_tokens=500,
    )

    text = response.choices[0].message.content.strip()
    print("OCR Extracted Text:", text)
    return text
