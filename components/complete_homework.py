from playwright.sync_api import Page
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def auto_accept(dialog):
    dialog.accept()
    #print("submitted Homework")


def organize_choices(choice_texts):
    lines = []
    for idx, text in enumerate(choice_texts):
        line = f"{idx + 1}. {text}"
        lines.append(line)
    return "\n".join(lines)


def complete_homework(page: Page):
    #print("Completing homework...")
    page.wait_for_load_state("domcontentloaded")
    questions = page.locator(".widget-body")
    count = questions.count()

    for i in range(1, count):
        question = questions.nth(i)

        p_tags = question.locator("p").all_inner_texts()
        q_text = " ".join(p_tags).strip()
        if not q_text:
            #print("No <p> tags found, trying .question-main-text-wrapper")
            p_tags = question.locator(".question-main-text-wrapper").all_inner_texts()
            q_text = " ".join(p_tags).strip()
            #print("Extracted text, original:", q_text, p_tags)

        choices = question.locator("div.answer label")
        choice_texts = []
        for choice in choices.all_inner_texts():
            cleanedChoice = choice.strip()
            if cleanedChoice:
                choice_texts.append(cleanedChoice)

        #print("Question:", q_text)
        #print("Choices:", choice_texts)

        if not choice_texts:
            #print(f"No choices found for question {i+1}, skipping.")
            continue

        prompt = f"""
        Question: {q_text}

        Choices:{organize_choices(choice_texts)}
            
        Reply with ONLY one number (1 to {len(choice_texts)}).
        Do not leave blank. If unsure, guess."""

        def ask_gpt():
            return client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are answering multiple choice questions. You must carefully choose the correct option based on the question. Your final reply must be only a single digit (1 to n).  No words, no punctuation, no explanations.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_completion_tokens=5,
            )

        response = ask_gpt()
        raw_answer = response.choices[0].message.content.strip()
        answer = next((ch for ch in raw_answer if ch.isdigit()), None)
        if not answer:
            #print(f"Chat gpt gave no valid answer to {q_text}. Retrying once")
            response = ask_gpt()
            raw_answer = response.choices[0].message.content.strip()
            answer = next((ch for ch in raw_answer if ch.isdigit()), None)
            if not answer:
                #print("Second try failed again. Picking random choice")
                answer = str(random.randint(1, len(choice_texts)))
        choices.nth(int(answer) - 1).click()

    page.once("dialog", auto_accept)
    page.locator("#submitbtn").click()
