from playwright.sync_api import Page
from components.complete_homework import complete_homework
from components.copy_homework_answers import extract_correct_answers
from components.retry_with_answers import retry_with_answers


def close_modal_if_exists(page: Page):
    print("Checking for modal...")
    page.wait_for_selector("#finishExamPopUp", timeout=30000)
    print("Modal found, attempting to close...")
    try:
        page.evaluate(
            """
            () => {
                const modal = document.querySelector('#finishExamPopUp');
                const overlay = document.querySelector('.modal-backdrop');
                if (modal) {
                    modal.style.display = 'none';
                    modal.classList.remove('in', 'show');
                    overlay.remove(); 
                }
            }
        """
        )
        print("Modal hidden")
    except Exception as e:
        print(f"Failed to hide modal: {e}")


def start_homework(page: Page):
    page.goto("https://me.classera.com/student/assignments/show_homework")
    page.wait_for_selector("text= | إعادة المحاولة", timeout=15000)
    page.wait_for_timeout(1000)

    homework_list = page.locator("text=بدء")
    if homework_list.count() == 0:
        print("No homework found, checking next page...")
        next_button = page.locator('.page-link >> text="التالي"')
        if next_button.count() > 0:
            next_button.click()
            page.wait_for_timeout(2000)
            homework_list = page.locator("text=بدء")
        else:
            print("No next button found, exiting...")
            return

    count = homework_list.count()

    for i in range(count):
        # nth = i if its "إعادة المحاولة", nth = 0 if its "بدء"
        homework = homework_list.nth(0)
        url = homework.get_attribute("url")
        full_url = "https://me.classera.com" + url

        page.goto(full_url)
        page.wait_for_timeout(1000)

        print(f"Opening homework {i+1}")
        page.locator('input[type="submit"][value="البدء"]').nth(1).click()
        complete_homework(page)

        text = page.text_content("div.final-mark-focus")
        print("Raw text:", text)
        nums = [int(word) for word in text.split() if word.isdigit()]
        first_num = nums[0] if len(nums) > 0 else None
        second_num = nums[1] if len(nums) > 1 else None
        accuracy = (first_num / second_num) * 100
        print(f"{accuracy:.1f}%")
        if accuracy < 90:
            print("Result less than 90%, Copying answers for retry...")
            close_modal_if_exists(page)
            data = extract_correct_answers(page, full_url)
            page.wait_for_load_state("domcontentloaded")
            retry_with_answers(full_url, page, data)
            print("finished retrying...")
        page.goto(
            "https://me.classera.com/student/assignments/show_homework#networkfirst"
        )
        page.wait_for_timeout(750)
        print("Done")
        page.wait_for_timeout(500)
