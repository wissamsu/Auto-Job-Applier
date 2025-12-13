from playwright.sync_api import Locator, sync_playwright

def main():
    with sync_playwright() as p: 
        context= p.chromium.launch_persistent_context(user_data_dir="profile",headless=False, slow_mo=800)

        
        page = context.new_page()
        # Go to linkedin
        page.goto("https://www.linkedin.com/jobs/")
        # Go to the search bar and type java
        page.get_by_placeholder("Describe the job you want").type("java")
        page.keyboard.press("Enter")
        # Apply the easy apply filter
        page.locator("label:has-text('Easy Apply')").wait_for(state="visible")  # reveal the checkbox
        page.locator("label:has-text('Easy Apply')").click(force=True)
        # Get the number of jobs
        JobsFound: Locator = page.locator("//*[@id='workspace']/div/div/div[1]/div/div[1]/div/div/div/div/div")
        print(JobsFound.count(), "jobs found")
        while(True):
            for i in range(0, JobsFound.count()):
                page.wait_for_timeout(1000)
                if(page.get_by_label("Easy Apply to this job").count() > 0 and page.get_by_label("Easy Apply to this job").is_visible()):
                    page.get_by_label("Easy Apply to this job").click(force=True)
                    #Click easy apply button
                    page.wait_for_timeout(1000)
                    if(page.get_by_label("Continue to next step").count() > 0 or page.get_by_label("Continue to next step").is_visible()):
                        print("reached 6")
                        page.get_by_label("Continue to next step").click(force=True)
                    #Skip first step since its already filled in
                    if(page.get_by_label("Continue to next step").count() > 0):
                        page.get_by_label("Continue to next step").click(force=True)
                    if(page.get_by_label("Review your application").count() > 0):
                        page.get_by_label("Review your application").click(force=True)
                    if(page.get_by_label("Submit application").count() > 0):
                        page.get_by_label("Submit application").click(force=True)
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
                                page.locator("label[data-test-text-selectable-option__label='Yes']").nth(j).click(force=True)
                        #Check if the next button is next or review
                        if(page.get_by_label("Review your application").count() > 0):
                            print("reached 5")
                            page.get_by_label("Review your application").dblclick(force=True)
                        if(page.get_by_label("Continue to next step").count() > 0):
                            print("reached 4")
                            page.get_by_label("Continue to next step").click(force=True)
                        
                    #Now submit the application
                    if(page.get_by_label("Submit application").count() > 0):
                        page.get_by_label("Submit application").click(force=True)
                    #Dismiss the your application was sent page
                    page.wait_for_timeout(1000)
                    page.locator("svg[data-test-icon='close-medium']").click(force=True)
                else:
                    print(f"You already applied to job number {i}")
                    JobsFound.nth(i).click(force=True) 
            #Go to next page of jobs
            if(page.locator("//*[@id='workspace']/div/div/div[1]/div/div[2]/button[2]/span/span").count() > 0):
                print("Used first")
                page.locator("//*[@id='workspace']/div/div/div[1]/div/div[2]/button[2]/span/span").click(force=True)
                print("Used next button")
                page.wait_for_timeout(5000)
            else:
                break




if __name__ == "__main__":
    main()

