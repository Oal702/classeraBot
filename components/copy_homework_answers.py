from playwright.sync_api import Playwright, Page


def extract_correct_answers(page: Page, URL: str) -> list[str]:
    print("Extracting correct answers...")

    raw_answer_fields = page.locator(".correct-answer-table")
    count = raw_answer_fields.count()
    answers = []

    for i in range(count):
        field = raw_answer_fields.nth(i).locator("p")
        p_count = field.count()

        if p_count >= 2:
            answer_text = field.nth(1).inner_text().strip()
        elif p_count >= 1:
            answer_text = field.first.inner_text().strip()
        else:
            print(f"Skipping field {i}, no <p> tags found")
            continue

        if answer_text:
            answers.append(answer_text)
            print(f"Found answer field: {answer_text}")
            print(f"current answer list: {answers}")

    return answers
