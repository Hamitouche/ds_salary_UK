from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

      
def fetch_jobs(path,location, keyword, num_jobs):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    #Initialize the webdriver
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service = service)
    driver.set_window_size(1120, 1000)
    location = location.lower().replace(' ', '-')
    keyword = keyword.lower().replace(' ', '-')
    url = "https://www.glassdoor.com/Job/"+location+"-"+keyword+"-jobs-SRCH_IL.0,13_IN1_KO14,27.htm"
    driver.get(url)
    #Intialize list to contain scrape data
    jobs = []
    
    #Set current page to 1
    current_page = 1     
    while len(jobs) < num_jobs: 
        time.sleep(15)
        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
        except ElementClickInterceptedException:
            print('selected not found')
            pass

        time.sleep(.1)

        #Closes the signup prompt
        try :
            driver.find_element(By.CSS_SELECTOR, "button[class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']").click()  #clicking to the X.
        except NoSuchElementException:
                print(' x out failed')
                pass
        job_cards = driver.find_elements(By.XPATH,"//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
      
        for card in job_cards:
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs))) 
            if len(jobs) > num_jobs:
                break 
            card.click()
            time.sleep(1)
            #Scrape 
            collected_successfully = False
            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH,"//div[@data-test='employerName']").text
                    job_title = driver.find_element(By.XPATH,"//div[@data-test='jobTitle']").text
                    location = driver.find_element(By.XPATH,"//div[@data-test='location']").text
                    job_description = driver.find_element(By.XPATH,"//div[@id='JobDescriptionContainer']").text
                    collected_successfully = True
                except:
                    time.sleep(5)
            
            try:
                salary_estimate = driver.find_element(By.XPATH,"//span[@data-test='detailSalary']").text
            except:
                continue
            try:
                company_size = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text
            except:
                company_size = "N/A"
                pass
            
            try:
                company_type = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text
            except:
                company_type = "N/A"
                pass
                
            try:
                company_sector = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text
            except:
                company_sector = "N/A"
                pass
                
            try:
                company_industry = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text
            except:
                company_industry = "N/A"
                pass
                
            try:
                company_founded = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text
            except:
                company_founded = "N/A"
                pass

            #Add job to jobs list
            jobs.append({'company': company_name, 
                'job title': job_title,
                'location': location,
                'job description': job_description,
                'salary estimate': salary_estimate,
                'company_size': company_size,
                'company_type': company_type,
                'company_sector': company_sector,
                'company_industry' : company_industry,
                'company_founded' : company_founded})
               
        # Move to the next page         
        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH,"//button[@data-test='pagination-next']").click()
            print(str(current_page) + ' page(s) done')
            current_page += 1
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
    
    driver.close()

    #Build the dataframe
    df = pd.DataFrame(jobs)
    
    #Export df to a csv file
    df.to_csv('jobs_test.csv')

PATH = "chromedriver.exe"                   
fetch_jobs(PATH, "United States", "Data Engineer", 800)