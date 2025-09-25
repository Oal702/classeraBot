from playwright.sync_api import sync_playwright

def sign_in():
    with sync_playwright() as p:
        # Launch Chromium with GUI and keep it open
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to login page
        page.goto("https://me.classera.com/student/users/login#networkfirst")

        # Fill login form (replace with your selectors)
        page.fill('input[name="data[User][username]"]', "aqs2s0573")
        page.fill('input[name="data[User][password]"]', "ACEDEF943f24")

        # Click the login button
        page.click('input[value="Login"]')

        # Wait for navigation or some element that proves login worked
        page.wait_for_load_state("networkidle")