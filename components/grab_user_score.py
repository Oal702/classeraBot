from playwright.sync_api import Page


def grab_user_score(page: Page):
    page.goto("https://me.classera.com")
    try:
        score = page.locator("a.score-link").nth(1).text_content(timeout=5000)
    except Exception as e:
        print(f"Error grabbing user score: {e}")
        score = page.locator("a.score-link").nth(0).text_content(timeout=10000)
    return score
