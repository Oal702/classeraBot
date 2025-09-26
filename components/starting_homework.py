from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://me.classera.com/student/users/login#networkfirst")

    # Fill login form (replace with your own username/password)
    page.fill('input[name="data[User][username]"]', "aqs2s0573")
    page.fill('input[name="data[User][password]"]', "ACEDEF943f24")

    # Click the login button
    page.click('input[value="Login"]')

    # Wait for login to finish
    page.wait_for_timeout(2000)

    # Go to homework page
    page.goto("https://me.classera.com/student/assignments/show_homework#networkfirst")
    page.wait_for_timeout(500)

    # Locate homework items
    hws = page.locator(".lunch_exam")
    count = hws.count()

    if count > 0:
        print(f"There are {count} homeworks you did not do!")
    else:
        print("You don't have any homeworks for now!")


    # Loop through all homeworks
    for i in range(count):
        hw = hws.nth(i)
        url = hw.get_attribute("url")  # relative exam URL
        full_url = "https://me.classera.com" + url


        # Open the exam
        page.goto(full_url)
        page.wait_for_timeout(250)

        print(f"Opening homework {i+1}")
        
        # Go back to homework list
        page.goto("https://me.classera.com/student/assignments/show_homework#networkfirst")
        page.wait_for_timeout(500)
        print("Done")
