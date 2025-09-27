import os
from playwright.sync_api import Page
from dotenv import load_dotenv

load_dotenv()


def sign_in(page: Page):
    username = os.getenv("CLASSERA_USERNAME")
    password = os.getenv("CLASSERA_PASSWORD")

    page.goto("https://me.classera.com/student/users/login#networkfirst", timeout=60000)
    page.wait_for_timeout(1000)
    page.fill('input[name="data[User][username]"]', username)
    page.fill('input[name="data[User][password]"]', password)

    page.click('input[value="Login"]')
    page.wait_for_timeout(1000)
