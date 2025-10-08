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


def start_homework(page: Page, pageNum):
    page.goto("https://me.classera.com/student/assignments/show_homework")
    print("Page: ", pageNum+1)
    if(pageNum > 0):
        page.click('a.page-link >> text="التالي"')
        page.wait_for_timeout(1500)
    
    page.wait_for_timeout(3000)

    homework_list = page.locator("text=بدء" or "text=إعادة المحاولة")

    count = homework_list.count()
    print("There is ", count, "homework")
    for i in range(count):

        # nth = i if its "إعادة المحاولة", nth = 0 if its "بدء"
        homework = homework_list.nth(0)
        url = homework.get_attribute("url")
        full_url = "https://me.classera.com" + url

        page.goto(full_url)
        page.wait_for_timeout(1000)

        print(f"Opening homework {i+1}", page.locator("li.last").inner_text().strip())
        page.locator('input[type="submit"][value="البدء"]').nth(1).click()
        complete_homework(page)
        try:
            text = page.text_content("div.final-mark-focus")
            #print("Raw text:", text)
            nums = [int(word) for word in text.split() if word.isdigit()]
            first_num = nums[0] if len(nums) > 0 else None
            second_num = nums[1] if len(nums) > 1 else None
            accuracy = (first_num / second_num) * 100
            print("The accuracy of " ,page.locator("li.last").inner_text().strip() ,": " ,f"{accuracy:.1f}%")
            if accuracy < 90:
                #print("Result less than 90%, Copying answers for retry...")
                close_modal_if_exists(page)
                data = extract_correct_answers(page, full_url)
                page.wait_for_load_state("domcontentloaded")
                retry_with_answers(full_url, page, data)
                #print("finished retrying...")
        except Exception as e:
            print(f"Error processing accuracy of question {i+1}: {e}")        

        page.goto("https://me.classera.com/student/assignments/show_homework#networkfirst")
        page.wait_for_timeout(1500)

        if(pageNum > 0):
            page.click('a.page-link >> text="التالي"')
            page.wait_for_timeout(1500)

        page.wait_for_timeout(750)
        print("Done")
        page.wait_for_timeout(500)
