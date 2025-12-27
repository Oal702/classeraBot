from playwright.sync_api import Page


def auto_accept(dialog):
    dialog.accept()
    print("✅ Submitted Homework")


def retry_with_answers(URL: str, page: Page, data: list[dict]):
    print("Retrying homework with stored question-answer data...")

    page.goto(URL)
    page.wait_for_load_state("domcontentloaded")
    page.locator('input[type="submit"][value="البدء"]').nth(1).click()
    page.wait_for_selector(".widget-body:visible", timeout=10000)

    questions = page.locator(
        ".widget-body:visible", has_not=page.locator(".announcement")
    )
    q_count = questions.count()
    homework_name = page.locator("li.last").inner_text().strip()
    print(f"Retrying homework: {homework_name}")
    print(f"Found {q_count} questions on page")

    for q_index in range(q_count):
        question = questions.nth(q_index)

        p_tags = question.locator(".question-main-text-wrapper").all_inner_texts()
        q_text = " ".join(p_tags).strip()
        if q_text.strip() == "":
            print("Question text is empty, checking for image...")
            img = question.locator("img").first
            if img.count() > 0:
                q_text = img.first.get_attribute("src")
        print(f"\n[Q{q_index+1}] {q_text}")

        matched_item = None
        for item in data:
            stored_q = item["question"].strip()
            if stored_q in q_text or q_text in stored_q:
                matched_item = item
                break

        if not matched_item:
            print(f"No stored match found for: {q_text[:60]}...")
            continue

        correct_answers = matched_item["answers"]
        if not correct_answers:
            print(f"No stored answers found for this question.")
            continue

        choices = question.locator("div.answer label")
        choice_count = choices.count()
        print(f"Found {choice_count} choices.")

        matched = False
        for choice_index in range(choice_count):
            choice = choices.nth(choice_index)
            choice_text = choice.inner_text().strip()
            if choice_text.strip() == "":
                print("Choice text is empty, checking for image...")
                img = choice.locator("img").first
                if img.count() > 0:
                    choice_text = img.first.get_attribute("src")
                    print(f"Extracted image src as choice text: {choice_text}")
            for correct in correct_answers:
                if choice_text.strip() == correct.strip():
                    choices.nth(choice_index).click()
                    matched = True
                    print(f"Clicked matching answer: {choice_text}")
                    break
            if matched:
                break

        if not matched:
            print(f"No choice matched for this question.")

    page.once("dialog", auto_accept)
    page.locator("#submitbtn").click()
