from playwright.sync_api import sync_playwright
from components.sign_in import sign_in
from components.start_homework import start_homework
from components.grab_user_score import grab_user_score
from dotenv import load_dotenv
from supabase import create_client, Client
from store import store
import json
import os


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def process_user(currentUser):
    try:
        store.reset()
        user_id = currentUser["id"]

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            context.grant_permissions(
                ["notifications"], origin="https://me.classera.com"
            )
            page = context.new_page()

            sign_in(page, currentUser)

            pageNum = 1
            while True:
                page.goto("https://me.classera.com/student/assignments/show_homework")

                current_page = page.locator("a.page-link", has_text=str(pageNum))
                try:
                    current_page.wait_for(state="visible", timeout=3000)
                except:
                    print("No more pages found. Ending pagination.")
                    break
                current_page.click()
                page.wait_for_timeout(1000)
                start_homework(page, pageNum)
                try:
                    next_li = page.locator("li#assignments_grid_next")
                    classes = next_li.get_attribute("class") or ""
                    if "disabled" in classes:
                        break
                except Exception as e:
                    print("Error locating next button:", e)
                    break

                next_li.locator("a").click()

                page.wait_for_selector("#assignments_grid_processing", state="hidden")
                pageNum += 1

            score = grab_user_score(page)
            store.set_score(score)

            JSON_data = store.to_json()
            print(JSON_data)

            if not JSON_data.get("homeworkList"):
                print("No homework data found. Skipping Supabase update for this user.")
                context.close()
                browser.close()
                return

            try:
                existing_rows = (
                    supabase.table("user_accounts")
                    .select("stats")
                    .eq("id", user_id)
                    .execute()
                    .data
                )
            except Exception as e:
                print("Error fetching existing data:", e)
                existing_rows = []

            try:
                if existing_rows and existing_rows[0].get("stats"):
                    print("Merging with existing data")
                    existing_stats = existing_rows[0]["stats"]
                    if isinstance(existing_stats, str):
                        existing_stats = json.loads(existing_stats)

                    # merge score and homework list
                    existing_stats["score"] = JSON_data["score"]
                    existing_stats.setdefault("homeworkList", []).extend(
                        JSON_data.get("homeworkList", [])
                    )
                    JSON_data = existing_stats
            except Exception as e:
                print("Error merging data:", e)

            supabase.table("user_accounts").update({"stats": JSON_data}).eq(
                "id", user_id
            ).execute()
            context.close()
            browser.close()
    except Exception as e:
        print("An error occured: ", e)


def main():
    users = (
        supabase.table("user_accounts")
        .select("*")
        .eq("subscription_status", "Active")
        .execute()
        .data
    )
    for currentUser in users:
        process_user(currentUser)


if __name__ == "__main__":
    main()
