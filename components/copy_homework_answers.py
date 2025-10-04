from playwright.sync_api import Page


def extract_correct_answers(page: Page, URL: str) -> list[dict]:
    print("Extracting questions and answers...")

    question_blocks = page.locator(".question")
    question_count = question_blocks.count()
    data = []

    for i in range(question_count):
        block = question_blocks.nth(i)
        if not block.locator("p").count():
            print(f"Skipping ghost question block #{i+1}")
            continue
        question_locator = block.locator(".question-main-text-wrapper, .questionBody")
        if question_locator.count() > 0:
            p_tags = question_locator.all_inner_texts()
            question_text = " ".join(p_tags).strip()
        else:
            question_locator = block.locator(
                "p strong, p span strong, p span span strong, p * strong"
            )
            if question_locator.count() > 0:
                question_text = question_locator.first.inner_text().strip()
            else:
                question_text = block.locator("p").first.inner_text().strip()

        answer_fields = block.locator(".correct-answer-table")
        answer_count = answer_fields.count()
        answers = []

        for j in range(answer_count):
            field = answer_fields.nth(j).locator("p")
            p_count = field.count()

            if p_count >= 2:
                answer_text = field.nth(1).inner_text().strip()
            elif p_count >= 1:
                answer_text = field.first.inner_text().strip()
            else:
                continue

            if answer_text:
                answers.append(answer_text)

        data.append({"question": question_text, "answers": answers})

        print(f"Q{i+1}: {question_text}")
        print(f"Answers: {answers}")

    print(f"Returned data: {len(data)} questions.")
    return data
