from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

      
def fetch_jobs(path, keyword, num_pages):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    #Initialize the webdriver
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service = service)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="

    driver.get(url)
    
    #Intialize lists to contain scrape data
    company_name = []
    job_title = []
    location = []
    job_description = []
    salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_founded = []
    company_revenue = []
    
    
    
    #Set current page to 1
    current_page = 1     
    while current_page <= num_pages:   
        done = False
        while not done:
            job_cards = driver.find_elements(By.XPATH,"//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
            for card in job_cards:
                card.click()
                time.sleep(1)

                #Closes the signup prompt
                try :
                   driver.find_element(By.CSS_SELECTOR, "button[class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']").click()  #clicking to the X.
                except NoSuchElementException:
                   pass

                #Scrape 

                try:
                    company_name.append(driver.find_element(By.XPATH,"//div[@data-test='employerName']").text)
                except:
                    company_name.append("N/A")
                    pass

                try:
                    job_title.append(driver.find_element(By.XPATH,"//div[@data-test='jobTitle']").text)
                except:
                    job_title.append("N/A")
                    pass

                try:
                    location.append(driver.find_element(By.XPATH,"//div[@data-test='location']").text)
                except:
                    location.append("N/A")
                    pass

                try:
                    job_description.append(driver.find_element(By.XPATH,"//div[@id='JobDescriptionContainer']").text)
                except:
                    job_description.append("N/A")
                    pass

                try:
                    salary_estimate.append(driver.find_element(By.XPATH,"//span[@data-test='detailSalary']").text)
                except:
                    salary_estimate.append("N/A")
                    pass
                
                try:
                    company_size.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text)
                except:
                    company_size.append("N/A")
                    pass
                
                try:
                    company_type.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text)
                except:
                    company_type.append("N/A")
                    pass
                    
                try:
                    company_sector.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text)
                except:
                    company_sector.append("N/A")
                    pass
                    
                try:
                    company_industry.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text)
                except:
                    company_industry.append("N/A")
                    pass
                    
                try:
                    company_founded.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text)
                except:
                    company_founded.append("N/A")
                    pass
                    
                try:
                    company_revenue.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text)
                except:
                    company_revenue.append("N/A")
                    pass 
                done = True
                
        # Moves to the next page         
        if done: 
            #Clicking on the "next page" button
            try:
               driver.find_element(By.XPATH,"//button[@data-test='pagination-next']").click()
               print(str(current_page) + ' ' + 'out of' +' '+ str(num_pages) + ' ' + 'pages done')
               current_page += 1
            except NoSuchElementException:
               print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_pages, current_page))
               break
        time.sleep(4) 
    
    driver.close()

    #Build the dataframe
    df = pd.DataFrame({'company': company_name, 
    'job title': job_title,
    'location': location,
    'job description': job_description,
    'salary estimate': salary_estimate,
    'company_size': company_size,
    'company_type': company_type,
    'company_sector': company_sector,
    'company_industry' : company_industry,
    'company_founded' : company_founded, 
    'company_revenue': company_revenue})
    
    #Export df to a csv file
    df.to_csv('jobs.csv')

PATH = "chromedriver.exe"                   
fetch_jobs(PATH, "Data Engineer", 3)