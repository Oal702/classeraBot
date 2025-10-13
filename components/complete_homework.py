import base64
from playwright.sync_api import Page
import random
from openai import OpenAI
from dotenv import load_dotenv
import random
from components.helpers.answer_image_questions import extract_question_from_image
import os
import re

load_dotenv()
client = OpenAI()


def auto_accept(dialog):
    dialog.accept()
    print("submitted Homework")


def organize_choices(choice_texts):
    lines = []
    for idx, text in enumerate(choice_texts):
        line = f"{idx + 1}. {text}"
        lines.append(line)
    return "\n".join(lines)


def complete_homework(page: Page):
    # print("Completing homework...")
    page.wait_for_load_state("domcontentloaded")
    questions = page.locator(".widget-body:visible")
    count = questions.count()
    os.makedirs("runtime_images", exist_ok=True)

    for i in range(count + 1):
        try:
            question = questions.nth(i)
            question.wait_for(state="visible", timeout=5000)

            p_tags = question.locator(".question-main-text-wrapper").all_inner_texts()
            q_text = " ".join(p_tags).strip()

            img_count = question.locator("img").count()
            if not q_text or img_count > 0:
                # print(f"Checking for image in question {i+1} (imgs={img_count})...")
                img_path = os.path.join("runtime_images", f"screenshot_q{i+1}.png")
                page.wait_for_timeout(1500)
                question.screenshot(path=img_path)
                ocr_text = extract_question_from_image(img_path).strip()
                if ocr_text:
                    q_text = ocr_text
                    # print(f"Question {i+1} OCR extracted: {q_text}")

            choices = question.locator("div.answer label")
            choicesNum = question.locator("div.answer input").count()
            choice_texts = [c.strip() for c in choices.all_inner_texts() if c.strip()]

            # print("Question:", q_text)
            # print("Choices:", choice_texts)

            # if not choice_texts:
            # print(f"No choices found for question {i+1}, skipping.")

            prompt = f"""
            Question: {q_text}

            Choices:{organize_choices(choice_texts)}
                
            Reply with ONLY one number (1 to {len(choice_texts)}).
            Do not leave blank. If unsure, guess."""

            def ask_gpt():
                return client.chat.completions.create(
                    model="gpt-4.1-nano",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are answering high-school level multiple-choice questions across multiple subjects. "
                                "Always reply ONLY in this format:\n"
                                "explanation: <short reasoning>\n"
                                "final answer: <digit from 1 to n>"
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                    max_completion_tokens=300,
                )

            response = ask_gpt()
            raw_answer = response.choices[0].message.content.strip()
            match = re.search(r"final answer:\s*(\d+)", raw_answer, re.IGNORECASE)
            answer = (
                match.group(1)
                if match
                else print(f"ChatGPT response format unexpected: {raw_answer}")
            )

            if not answer:
                # print(f"ChatGPT gave no valid answer to {q_text!r}. Retrying once.")
                response = ask_gpt()
                raw_answer = response.choices[0].message.content.strip()
                answer = next((ch for ch in raw_answer if ch.isdigit()), None)

            if not answer or not (1 <= int(answer) <= len(choice_texts)):
                # print("Second try failed again or out of range. Picking random choice.")
                answer = str(random.randint(1, int(choicesNum)))
            # print(f"chat gpt gave this answer for question {i+1}: {raw_answer}")
            choices.nth(int(answer) - 1).click(timeout=5000)
        except Exception as e:
            print(f"Error processing question {i+1}: {e}")
            continue

    page.once("dialog", auto_accept)
    page.locator("#submitbtn").click()
    try:
        marks = page.text_content("div.final-mark-focus")

        nums = [int(word) for word in marks.split() if word.isdigit()]
        first_num = nums[0] if len(nums) > 0 else None
        second_num = nums[1] if len(nums) > 1 else None

        # print("First:", first_num, type(first_num))
        # print("Second:", second_num, type(second_num))

        if first_num is not None and second_num not in (None, 0):
            accuracy = first_num / second_num * 100
            print(f"{accuracy:.1f}%")
            return count
        else:
            print("Cannot calculate accuracy: missing or zero total")
            return count
    except Exception as e:
        print(f"Error processing accuracy of question {i+1}: {e}")
        return count
