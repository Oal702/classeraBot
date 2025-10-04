from playwright.sync_api import Page
from skimage.metrics import structural_similarity as ssim
import cv2


def auto_accept(dialog):
    dialog.accept()
    print("submitted Homework")


def retry_with_answers(URL: str, page: Page, answers: list[str]):
    print("Retrying homework with copied answers...")

    page.goto(URL)
    page.wait_for_load_state("domcontentloaded")
    page.locator('input[type="submit"][value="البدء"]').nth(1).click()
    page.wait_for_selector(".widget-body:visible", timeout=10000)

    questions = page.locator(".widget-body:visible")
    q_count = questions.count()
    print(f"Found {q_count} questions on page")

    for q_index, answer in enumerate(answers):
        if q_index >= q_count:
            print(f"No question {q_index+1} found, skipping.")
            continue

        question = questions.nth(q_index)
        choices = question.locator("div.answer label")
        choice_count = choices.count()

        matched = False
        for choice_index in range(choice_count):
            choice_text = choices.nth(choice_index).inner_text().strip()
            if choice_text.strip() == answer.strip():
                choices.nth(choice_index).click()
                matched = True
                break

        if not matched:
            print(f"No match found for Q{q_index+1}, answer: {answer}")

    page.once("dialog", auto_accept)
    page.locator("#submitbtn").click()
