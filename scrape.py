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
        
def getSyllabus(year,regno):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version='104.0.5112.79').install()), options=chrome_options)

            extractTag = re.compile('lbl_[^\"]+')
            resList = []
            for i in tqdm(range(len(regno))):
                url = "https://campus.icu.ac.jp/public/ehandbook/PreviewSyllabus.aspx?year="+year+"&regno="+regno[i]+"&term="+regno[i][0]
                # Open site
                driver.get(url)
                driver.implicitly_wait(3)
                # Find course table (get page -> get main table -> find td with contents inside it -> )
                form = driver.find_elements(By.TAG_NAME,"form")
                contentTable = BeautifulSoup(form[0].get_attribute('innerHTML'),'lxml')
                rawText = contentTable.find_all('span')

                syllabusDict = {'regno':regno[i]}
                for x in rawText:
                    # Process Tag and content
                    tag = extractTag.findall(str(x))
                    tag = tag[0].replace('lbl_','')
                    if tag == 'references':
                        tag = 'ref'
                    # print(tag)
                    content = str(x).replace("<br/>",'\n')
                    content = re.sub('<[^>]+>','',content)
                    # Add to Dict
                    syllabusDict.update({tag:content.strip('\n')})
                resList.append(syllabusDict)

            return resList
        except:
            traceback.print_exc()
        finally:
            driver.quit()
            
def getELA():
    try: 
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version='104.0.5112.79').install()), options=chrome_options)

        url = "https://course-reg.icu.ac.jp/ela/stsch/show_schedule.shtml"
        # Open site (will be sent to SSO login)
        driver.get(url)
        driver.implicitly_wait(3)

        # Login to ICU SSO
        driver.find_element(By.NAME,"uname").send_keys(os.environ['ICU_ELA_ADDRESS'])
        driver.find_element(By.NAME,"pass").send_keys(os.environ['ICU_SSO_PASSWORD'])
        driver.find_element(By.XPATH,"/html/body/form/center/table/tbody/tr[4]/td[2]/input").click() 
        driver.implicitly_wait(3)

        table_list = []
        # TODO
        # update tags based on selected term
        section_list = ["20233_FR3","20233_FR4","20233_AS3","20233_AS4","20233_RW12","20233_RW34"]
        for section in section_list:
            tables = driver.find_elements(By.XPATH,'//*[@id="{}"]/table'.format(section))
            for i in tables:
                i = i.get_attribute('outerHTML')
                table_list.append(i)
        return table_list
    except:
        traceback.print_exc()
    finally:
        driver.quit()