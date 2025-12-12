from playwright.sync_api import Locator, sync_playwright, expect

def main():
    with sync_playwright() as p: 
        browser= p.chromium.launch(headless=False, slow_mo=500)

        context = browser.new_context()

        context.add_cookies([{
            "name": "li_at",
            "value": "your_li_at_linkedin_cookie_value",
            "domain": "www.linkedin.com",
            "path": "/",
            "secure": True,
            "httpOnly": False
            }
        ])
        page = context.new_page()
        # Go to linkedin
        page.goto("https://www.linkedin.com/jobs/")
        # Go to the search bar and type java
        page.get_by_placeholder("Describe the job you want").type("what_job_you_want_goes_here")
        page.keyboard.press("Enter")
        # Apply the easy apply filter
        page.locator("label:has-text('Easy Apply')").wait_for(state="visible")  # reveal the checkbox
        page.locator("label:has-text('Easy Apply')").click()
        # Get the number of jobs
        JobsFound: Locator = page.locator("//*[@id='workspace']/div/div/div[1]/div/div[1]/div/div/div/div/div")
        print(JobsFound.count(), "jobs found")
        while(True):
            for i in range(0, JobsFound.count()):
                page.wait_for_timeout(1000)
                if(page.get_by_label("Easy Apply to this job").count() > 0 and page.get_by_label("Easy Apply to this job").is_visible()):
                    #Click easy apply button
                    page.get_by_label("Easy Apply to this job").click()
                    #Skip first step since its already filled in
                    page.get_by_label("Continue to next step").click()
                    if(page.get_by_label("Continue to next step").count() > 0):
                        page.get_by_label("Continue to next step").click()
                    if(page.get_by_label("Review your application").count() > 0):
                        page.get_by_label("Review your application").click()
                    if(page.get_by_label("Submit application").count() > 0):
                        page.get_by_label("Submit application").click()
                    #Check for any textboxes that need to be filled
                    while(page.get_by_label("Continue to next step").count() > 0 or page.get_by_label("Review your application").count() > 0):
                        print("filling")
                        if(page.get_by_role("textbox").count() > 0):
                            print("reached 1")
                            for j in range(0, page.get_by_role("textbox").count()):
                                page.get_by_role("textbox").nth(j).fill("3")
                        if(page.get_by_role("combobox").count() > 0):
                            print("reached 2")
                            for j in range(0, page.get_by_role("combobox").count()):
                                page.get_by_role("combobox").nth(j).select_option(label="Yes")
                        if(page.locator("label[data-test-text-selectable-option__label='Yes']").count() > 0):
                            print("reached 3")
                            for j in range(0, page.locator("label[data-test-text-selectable-option__label='Yes']").count()):
                                page.locator("label[data-test-text-selectable-option__label='Yes']").nth(j).click()
                        #Check if the next button is next or review
                        if(page.get_by_label("Continue to next step").count() > 0):
                            print("reached 4")
                            page.get_by_label("Continue to next step").click()
                        if(page.get_by_label("Review your application").count() > 0):
                            print("reached 5")
                            page.get_by_label("Review your application").click()
                    #Now submit the application
                    page.get_by_label("Submit application").click()
                    #Dismiss the your application was sent page
                    page.wait_for_timeout(1000)
                    page.locator("svg[data-test-icon='close-medium']").click()
                else:
                    print(f"You already applied to job number {i}")
                    JobsFound.nth(i).click() 
            #Go to next page of jobs
            if(page.locator("//*[@id='workspace']/div/div/div[1]/div/div[2]/button[2]").count() > 0):
                page.locator("//*[@id='workspace']/div/div/div[1]/div/div[2]/button[2]").click()
            else:
                break




if __name__ == "__main__":
    main()
