import os
from playwright.sync_api import sync_playwright
from components.sign_in import sign_in
from components.start_homework import start_homework
from components.enter_morfaqaat import enter_morfaqaat
from dotenv import load_dotenv

load_dotenv()

def main():
    users = int(os.getenv('USERS'))
    for currentUser in range(users):
        if(currentUser < 7):
            continue
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            pageNum = 0

            sign_in(page, currentUser)
            start_homework(page, pageNum)

            
            
            while(True):
                page.text_content('div#assignments_grid_info.dataTables_info')
                #print("Raw text:", page.text_content('div#assignments_grid_info.dataTables_info'))
                nums = [int(word) for word in page.text_content('div#assignments_grid_info.dataTables_info').split() if word.isdigit()]
                first_num = nums[1] if len(nums) > 1 else None
                second_num = nums[2] if len(nums) > 2 else None
                #print(first_num, second_num)
                if(second_num > first_num):
                    pageNum = pageNum + 1 
                    start_homework(page, pageNum)
                else:
                    break 
            
            #enter_morfaqaat(page)


if __name__ == "__main__":
    main()
