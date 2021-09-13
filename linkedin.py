import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
options = Options()
dataFloderPath = os.path.join('C:/Users/RDATS/Desktop/Projects/Data')
driver = webdriver.Chrome(executable_path=r"C:\\Users\\RDATS\\Desktop\\Projects\\driver\\chromedriver.exe")
keyword = open('keyword.txt', 'r')
files = keyword.readlines()
email = "sawkumarraoshan@gmail.com"
password = "rdat1234"
data = []
def login():
    url = "https://www.linkedin.com/"
    driver.get(url)
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.find_element_by_id('session_key').send_keys(email)
    driver.find_element_by_id('session_password').send_keys(password)
    driver.find_element_by_class_name('sign-in-form__submit-button').click()
    driver.implicitly_wait(5)
    url = "https://www.linkedin.com/jobs/"
    driver.get(url)
    # driver.find_element_by_id('ember23').click()
    driver.implicitly_wait(5)
 
def extractData():
    for subcategory in files:
        driver.implicitly_wait(5)
        '''Information_Technology_Software_SubCategory search one by one.......................'''

        driver.find_element_by_css_selector("input[class='jobs-search-box__text-input jobs-search-box__keyboard-text-input']").send_keys(subcategory)
        driver.find_element_by_xpath('//*[@id="global-nav-search"]/div/div[2]/button[1]').click()
        driver.implicitly_wait(5)

        '''details link extract data...............'''
        def GetDetailsOfItem(YPLink):
            print(YPLink)
            driver.get(YPLink)
            driver.implicitly_wait(10)
            try:
                companyIsItLocated = driver.find_element_by_class_name('jobs-unified-top-card__bullet').text
                print(companyIsItLocated)
            except:
                companyIsItLocated = ""    
            try:
                numberOfEmployees = driver.find_element_by_xpath("//div[@class='mt5 mb2']/div[2]/span").text
                print(numberOfEmployees)
            except:
                numberOfEmployees = ""    
            
            try:
                companiesDescription = driver.find_element_by_xpath("//p[@class='t-14 mt5']").text
                print(companiesDescription)
            except:
                companiesDescription = " "    
            driver.implicitly_wait(10)
                
            return pd.Series([companiesDescription, numberOfEmployees, companyIsItLocated])

        '''total count data.............'''
        
        text = driver.find_element_by_xpath("//small[@class='display-flex t-12 t-black--light t-normal']").text.strip("results")
        driver.implicitly_wait(30)
        comma = text.replace(',', '')
        totalCount = int(comma)
        print(totalCount)
        loops = int(totalCount/25)
        print(loops)
        print("loops successfully")
        '''loop running................'''
        # for lo in range(loops):
        for lo in range(2):
            actions = ActionChains(driver)
            time.sleep(5)

            '''Scraping data like jobPosition, companyofferingtheJob, Location and also detailsLink '''

            for prod in driver.find_elements_by_class_name("occludable-update"):
                actions.move_to_element(prod).perform()
                Position = prod.find_element_by_class_name('job-card-list__title').text
                print(Position)
                companyName = prod.find_element_by_class_name('job-card-container__company-name').text
                print(companyName)
                Location = prod.find_element_by_class_name('job-card-container__metadata-wrapper').find_element_by_class_name("job-card-container__metadata-item").text
                print(Location)
                detailsLink = prod.find_element_by_class_name("job-card-list__title").get_attribute('href')
                print(detailsLink)

                '''Data Append.........................................'''
                data.append([companyName, Position, Location, detailsLink])

            '''next page link or see more jobs link'''  
            print("Pagination==============================================================")
            try:
                current_page_number = driver.find_element_by_css_selector("li[class='artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view']").text
                pagenumber = int(current_page_number)
                print(f"Processing page {current_page_number}..")
                next_page_link = driver.find_element_by_css_selector("li[class='artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view']").find_element_by_xpath(f'//button[span = "{pagenumber + 1}"]')
                print(next_page_link)
                next_page_link.click()
            except NoSuchElementException:
                print(f"Exiting. Last page: {current_page_number}.")
                break
        if loops == 0:
            driver.close()
            pass
        else:
            datadf = pd.DataFrame(data, columns=['companyName', 'Position', 'Location', 'detailsLink'])
            datadf.to_csv(os.path.join(dataFloderPath, 'linkedin.csv'), index=False)  
            if len(datadf) == 0:
                driver.close()
            else:
                datadf[['companiesDescription','NumberOfEmployees', 'companyIsItLocated']] = datadf[['detailsLink']].apply(lambda x: GetDetailsOfItem(x[0]), axis=1)
                datadf = datadf[['companyName', 'Position', 'Location', 'companiesDescription','NumberOfEmployees', 'companyIsItLocated']]
                datadf.to_csv(os.path.join(dataFloderPath, 'linkedinDetails.csv'), index=False)
                driver.close()
                print(".....Successfully Completed...........")   
        
login()
extractData()        