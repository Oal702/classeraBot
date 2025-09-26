from playwright.sync_api import Page
from components.complete_homework import complete_homework


def start_homework(page: Page):
    page.goto("https://me.classera.com/student/assignments/show_homework#networkfirst")
    page.wait_for_timeout(500)

    homework_list = page.locator("text=بدء")
    count = homework_list.count()

    # Loop through all homework
    for i in range(count):
        homework = homework_list.nth(i)
        url = homework.get_attribute("url")  # relative exam URL
        full_url = "https://me.classera.com" + url

        page.goto(full_url)
        page.wait_for_timeout(1000)

        print(f"Opening homework {i+1}")
        page.locator('input[type="submit"][value="البدء"]').nth(1).click()
        complete_homework(page)

        # Go back to homework list
        page.goto("https://me.classera.com/student/assignments/show_homework#networkfirst")
        page.wait_for_timeout(750)
        print("Done")
        page.wait_for_timeout(500)
