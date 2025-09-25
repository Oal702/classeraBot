from playwright.sync_api import sync_playwright

def sign_in(page):
    # Go to login page
    page.goto("https://me.classera.com/student/users/login#networkfirst")

    # Fill login form (replace with your selectors)
    page.fill('input[name="data[User][username]"]', "aqs2s0573")
    page.fill('input[name="data[User][password]"]', "ACEDEF943f24")

    # Click the login button
    page.click('input[value="Login"]')
        
    # Wait for navigation or some element that proves login worked

    page.wait_for_timeout(3000)
        
        

def homeworks_page(page):
    #Go to homeworks page
    page.goto("https://me.classera.com/student/assignments/show_homework#networkfirst")

    page.wait_for_timeout(4000)

def sign_in_to_homeworks_page(page):

    sign_in(page)

    homeworks_page(page)