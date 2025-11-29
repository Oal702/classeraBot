from playwright.sync_api import sync_playwright
from components.sign_in import sign_in
from components.start_homework import start_homework
from components.grab_user_score import grab_user_score
from store import store
import json


def process_user(username, password):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            currentUser = {"username": username, "password": password}

            sign_in(page, currentUser)

            pageNum = 1
            while True:
                page.goto("https://me.classera.com/student/assignments/show_homework")

                current_page = page.locator("a.page-link", has_text=str(pageNum))
                try:
                    current_page.wait_for(state="visible", timeout=3000)
                except:
                    print("No more pages found. Ending pagination.")
                    break
                current_page.click()
                page.wait_for_timeout(1000)
                start_homework(page, pageNum)
                try:
                    next_li = page.locator("li#assignments_grid_next")
                    classes = next_li.get_attribute("class") or ""
                    if "disabled" in classes:
                        break
                except Exception as e:
                    print("Error locating next button:", e)
                    break

                next_li.locator("a").click()
                page.wait_for_selector("#assignments_grid_processing", state="hidden")
                pageNum += 1

            browser.close()
    except Exception as e:
        print("An error occured: ", e)


def main():
    #   You could also do:
    #    username = "Your Classera Username"
    #    password = "Your Classera Password"
    username = input("Enter username: ")
    password = input("Enter password: ")
    process_user(username, password)


if __name__ == "__main__":
    main()
