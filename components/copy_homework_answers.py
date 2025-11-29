from playwright.sync_api import Page


def extract_correct_answers(page: Page, URL: str) -> list[dict]:
    page.wait_for_load_state("domcontentloaded")
    print("Extracting questions and answers...")
    question_blocks = page.locator(
        ".question", has_not=page.locator(".announcement, div.final-mark-focus")
    )
    question_count = question_blocks.count()
    data = []

    for i in range(question_count):
        block = question_blocks.nth(i)
        question_block = block.locator(".question-main-text-wrapper, .questionBody")
        if question_block.count() > 0:
            p_tags = question_block.locator("p").all_inner_texts()
            question_text = " ".join(p_tags).strip()
            if question_text == "":
                img = question_block.locator("img")
                question_text = img.get_attribute("src")
                if not question_text:
                    print(
                        f"Could not extract question text for question {i+1}, skipping."
                    )
                    continue
        else:
            print(f"Could not find question block for question {i+1}, skipping.")
            continue

        answer_fields = block.locator(".correct-answer-table")
        answer_count = answer_fields.count()
        answers = []

        for j in range(answer_count):
            actual_feild = answer_fields.nth(j)
            text_field = answer_fields.nth(j).locator("p")
            p_count = text_field.count()

            if p_count >= 2:
                answer_text = text_field.nth(1).inner_text().strip()
            elif p_count >= 1:
                answer_text = text_field.first.inner_text().strip()
            else:
                continue

            if answer_text:
                answers.append(answer_text)
            else:
                img = actual_feild.locator("img")
                if img.count() > 0:
                    answer_text = img.first.get_attribute("src")
                    if answer_text:
                        answers.append(answer_text)

        data.append({"question": question_text, "answers": answers})

        print(f"Q{i+1}: {question_text}")
        print(f"Answers: {answers}")

    print(f"Returned data: {len(data)} questions.")
    return data
