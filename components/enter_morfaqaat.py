from playwright.sync_api import Playwright, Page


def enter_morfaqaat(page: Page):
    page.goto("https://me.classera.com/student/courses/materials_list")
    page.wait_for_selector("text=تنزيل", timeout=15000)
    table = page.locator("#grid_grid")
    material_button_list = table.locator(".btn.btn-grid")
    count = material_button_list.count()
    for i in range(count):
        material_button = material_button_list.nth(i)
        material_button.click()
        page.wait_for_timeout(3000)
        page.go_back()
        page.wait_for_timeout(3000)
