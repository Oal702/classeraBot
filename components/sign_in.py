import os
from playwright.sync_api import Page
from dotenv import load_dotenv

load_dotenv()


def sign_in(page: Page, currentUser):
    print(f"CLASSERA_USERNAME{currentUser+1}",f"CLASSERA_PASSWORD{currentUser+1}")
    username = os.getenv(str(f"CLASSERA_USERNAME{currentUser+1}"))
    password = os.getenv(str(f"CLASSERA_PASSWORD{currentUser+1}"))
    print(username, password)

    page.goto("https://me.classera.com/student/users/login#networkfirst", timeout=60000)
    page.wait_for_timeout(1000)
    page.fill('input[name="data[User][username]"]', username)
    page.fill('input[name="data[User][password]"]', password)

    page.click('input[value="Login"]')
    page.wait_for_timeout(1000)
