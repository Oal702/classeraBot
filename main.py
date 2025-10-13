from playwright.sync_api import sync_playwright
from components.sign_in import sign_in
from components.start_homework import start_homework
from components.grab_user_score import grab_user_score
from dotenv import load_dotenv
from supabase import create_client, Client
from store import store
import json

SUPABASE_URL = "https://abduwracofdicgjnklvm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiZHV3cmFjb2ZkaWNnam5rbHZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk5MzU4MzYsImV4cCI6MjA3NTUxMTgzNn0.rkPBO_Ox1Mr9xaN02JJWrXk_FSrzD5v3Tc-CM9bk6Ps"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

load_dotenv()


def main():
    users = supabase.table("user_accounts").select("*").execute().data
    for currentUser in users:
        store.reset()
        user_id = currentUser["id"]
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            pageNum = 0

            sign_in(page, currentUser)
            start_homework(page, pageNum)

            while True:
                page.text_content("div#assignments_grid_info.dataTables_info")
                nums = [
                    int(word)
                    for word in page.text_content(
                        "div#assignments_grid_info.dataTables_info"
                    ).split()
                    if word.isdigit()
                ]
                first_num = nums[1] if len(nums) > 1 else None
                second_num = nums[2] if len(nums) > 2 else None

                if second_num > first_num:
                    pageNum = pageNum + 1
                    start_homework(page, pageNum)
                else:
                    break

            score = grab_user_score(page)
            store.set_score(score)
            JSON_data = store.to_json()
            print(JSON_data)
            if not JSON_data.get("homeworkList"):
                print("No homework data found. skipping Supabase update.")
                return
            try:
                existing_data = (
                    supabase.table("user_accounts")
                    .select("stats")
                    .eq("id", user_id)
                    .execute()
                    .data
                )
                print("Existing data:", existing_data)
            except Exception as e:
                print("Error fetching existing data:", e)
                existing_data = None

            try:
                if existing_data and existing_data[0]["stats"]:
                    print("Merging with existing data")
                    existing_stats = existing_data[0]["stats"]
                    if isinstance(existing_stats, str):
                        existing_stats = json.loads(existing_stats)
                    existing_stats["score"] = JSON_data["score"]
                    existing_stats["homeworkList"].extend(JSON_data["homeworkList"])
                    JSON_data = existing_stats
            except Exception as e:
                print("Error merging data:", e)
            supabase.table("user_accounts").update({"stats": JSON_data}).eq(
                "id", user_id
            ).execute()


if __name__ == "__main__":
    main()
