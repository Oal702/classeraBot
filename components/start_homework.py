from playwright.sync_api import Page
from components.complete_homework import complete_homework
from components.copy_homework_answers import extract_correct_answers
from components.retry_with_answers import retry_with_answers
from store import store
from datetime import datetime


def close_modal_if_exists(page: Page):
    print("Checking for modal...")
    page.wait_for_timeout(500)
    try:
        if page.locator("#finishExamPopUp").is_visible():
            page.evaluate(
                """
                () => {
                    const modal = document.querySelector('#finishExamPopUp');
                    const overlay = document.querySelector('.modal-backdrop');
                    if (modal) {
                        modal.style.display = 'none';
                        modal.classList.remove('in', 'show');
                        overlay?.remove();
                    }
                }
                """
            )
            print("Modal hidden")
        else:
            print("No modal found")
    except Exception as e:
        print(f"Failed to hide modal: {e}")


def start_homework(page: Page, pageNum: int):
    page.goto("https://me.classera.com/student/assignments/show_homework")
    print("Page:", pageNum + 1)

    if pageNum > 0:
        page.get_by_text("التالي").click()
        page.wait_for_timeout(1500)

    page.wait_for_timeout(3000)

    homework_list = page.locator("tr", has_text="بدء")
    count = homework_list.count()
    print("There is", count, "homework")

    for i in range(count):
        homework = homework_list.nth(0)
        subject = homework.locator("td").nth(1).inner_text().strip()
        url = homework.locator("a", has_text="بدء").get_attribute("url")
        full_url = "https://me.classera.com" + url

        page.goto(full_url)
        page.wait_for_timeout(1000)

        name = page.locator("li.last").inner_text().strip()
        print(f"Opening homework {i + 1}: {name}")

        page.locator('input[type="submit"][value="البدء"]').nth(1).click()
        questions = complete_homework(page)

        try:
            close_modal_if_exists(page)
            text = page.text_content("div.final-mark-focus")
            nums = [int(word) for word in text.split() if word.isdigit()]
            first_num = nums[0] if len(nums) > 0 else None
            second_num = nums[1] if len(nums) > 1 else None
            accuracy = (first_num / second_num) * 100 if second_num else 0

            print(f"The accuracy of {name}: {accuracy:.1f}%")

            if accuracy < 90:
                data = extract_correct_answers(page, full_url)
                page.wait_for_load_state("domcontentloaded")
                if not data:
                    print("No stored answers found, skipping retry.")
                    continue
                new_accuracy = str(retry_with_answers(full_url, page, data)) + "%"
                page.wait_for_load_state("domcontentloaded")
                print(f"New accuracy after retry: {new_accuracy}")
                close_modal_if_exists(page)
                text = page.text_content("div.final-mark-focus")
                try:
                    name_locator = page.locator("td", has_text="عنوان الإختبار")
                    if not name_locator.count():
                        name_locator = page.locator("td", has_text="عنوان الاختبار")

                    homework_name = name_locator.locator("~ td").inner_text().strip()

                except Exception as e:
                    print("Error getting homework name:", e)
                    homework_name = "Unknown"
                score_text = (
                    page.locator("td", has_text="النقاط")
                    .locator("~ td")
                    .inner_text()
                    .strip()
                )
                store.add_homework(
                    {
                        "title": homework_name,
                        "subject": subject,
                        "accuracy": new_accuracy,
                        "score": score_text,
                        "completionDate": datetime.now().strftime("%Y-%m-%d"),
                    }
                )
                store.add_question(questions)
            else:
                close_modal_if_exists(page)
                homework_name = (
                    page.locator("td", has_text="عنوان الإختبار")
                    .locator("~ td")
                    .inner_text()
                    .strip()
                )
                score_text = (
                    page.locator("td", has_text="النقاط")
                    .locator("~ td")
                    .inner_text()
                    .strip()
                )
                print(f"Score text: {score_text}. Adding hoemwork to store")
                store.add_homework(
                    {
                        "title": homework_name,
                        "subject": subject,
                        "accuracy": f"{accuracy:.1f}%",
                        "score": int(score_text) if score_text.isdigit() else 0,
                        "completionDate": datetime.now().strftime("%Y-%m-%d"),
                    }
                )
                print(f"Recorded homework: {homework_name} with score {score_text}")

        except Exception as e:
            print(f"Error processing accuracy of question {i + 1}: {e}")

        page.goto(
            "https://me.classera.com/student/assignments/show_homework#networkfirst"
        )
        page.wait_for_timeout(1500)

        if pageNum > 0:
            page.get_by_text("التالي").click()
            page.wait_for_timeout(1500)

        page.wait_for_timeout(750)
        print("Done\n")
        page.wait_for_timeout(500)
