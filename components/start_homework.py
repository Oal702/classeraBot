from playwright.sync_api import Page
from components.complete_homework import complete_homework


def start_homework(page: Page):
    page.goto("https://me.classera.com/student/assignments/show_homework")
    page.wait_for_selector("text= | إعادة المحاولة", timeout=15000)
    page.wait_for_selector("text= | إعادة المحاولة", timeout=15000)

    homework_list = page.locator("text= | إعادة المحاولة")
    count = homework_list.count()

    for i in range(count):
        # nth = i if its "إعادة المحاولة", nth = 0 if its "بدء"
        homework = homework_list.nth(i)
        url = homework.get_attribute("url")
        full_url = "https://me.classera.com" + url

        page.goto(
            "https://me.classera.com/student/courses/homework_info/cid:revhpiSV5bel_e21L6rnQgC1E9/aid:ER1BN4vCGNysK9FBf33q6gC1E9"
        )
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

        page.goto(
            "https://me.classera.com/student/assignments/show_homework#networkfirst"
        )
        page.wait_for_timeout(750)
        print("Done")
        page.wait_for_timeout(500)
