from playwright.sync_api import sync_playwright
from components.sign_in import sign_in
from components.start_homework import start_homework
from components.enter_morfaqaat import enter_morfaqaat


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        sign_in(page)
        start_homework(page)
        enter_morfaqaat(page)
        print("finished everything!")


if __name__ == "__main__":
    main()
