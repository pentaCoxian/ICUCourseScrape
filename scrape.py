import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import re
import os 
from dotenv import load_dotenv
import time

load_dotenv()

# Chrome settings
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito") #don't want cache
chrome_options.add_argument("--headless")

def getCourses(value = "all"):
    try: 
        # service = Service(ChromeDriverManager(version='114.0.5735.90').install()) 
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        # service = Service()
        # driver = webdriver.Chrome(service=service, options=chrome_options)

        #use driver_version as given in README
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version='104.0.5112.79').install()), options=chrome_options)

        url = "https://campus.icu.ac.jp/icumap/ehb/SearchCO.aspx"

        # Open site (will be sent to SSO login)
        driver.get(url)
        driver.implicitly_wait(3)

        # Login to ICU SSO
        driver.find_element(By.ID,"username_input").send_keys(os.environ['ICU_SSO_ADDRESS'])
        driver.find_element(By.ID,"password_input").send_keys(os.environ['ICU_SSO_PASSWORD'])
        driver.find_element(By.ID,"login_button").click()
        driver.implicitly_wait(3)

        # Select show ALL results to get full course list
        select_element = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_ddlPageSize")
        select_object = Select(select_element)
        select_object.select_by_visible_text("ALL")

        if value == "all":
            pass
        else:
            term_element = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_ddl_term")
            term_object = Select(term_element)
            term_object.select_by_visible_text(value)
        
        driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_btn_search").click()
        driver.implicitly_wait(3)

        # Find course table
        tables = driver.find_elements(By.TAG_NAME,"table")
        course_table = tables[3].get_attribute('innerHTML')
        #print(course_table)
        return course_table
    except:
        traceback.print_exc()
    finally:
        driver.quit()