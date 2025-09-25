from playwright.sync_api import sync_playwright
from components.sign_in_to_homeworks_page import sign_in_to_homeworks_page
from components.home_page_nav import home_page_nav


def main():
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        sign_in_to_homeworks_page(page)


if __name__ == "__main__":
    main()
