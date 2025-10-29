from playwright.async_api import async_playwright
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/signup")
async def signup(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    print("Received:", data)
    print("Username:", username, "Password:", password)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(
            "https://me.classera.com/student/users/login#networkfirst", timeout=60000
        )
        await page.wait_for_timeout(1000)
        await page.fill('input[name="data[User][username]"]', username)
        await page.fill('input[name="data[User][password]"]', password)
        await page.click('input[value="Login"]')

        try:
            await page.wait_for_selector(".circle_empty", timeout=30000)
            result = {"success": "success"}
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        finally:
            await browser.close()

    return result


if __name__ == "__main__":
    uvicorn.run(
        "components.validate_account_API:app", host="0.0.0.0", port=8080, reload=True
    )
