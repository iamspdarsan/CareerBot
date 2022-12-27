from datetime import datetime
import json
import os
import shutil
import sys
from selenium.webdriver.common.by import By
import selenium.common.exceptions as ex
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


userdir=os.getcwd()+'\\userdata'
qlfile='userdata\\filteredqlink'


def logwriter(log):
    with open('log.txt','a') as logfile:
        logfile.writelines(f"{log} | {getdatetime()}\n")


def getdatetime():
    return datetime.now().strftime('%d:%m:%Y - %I:%M:%S:%p')


def close_chatbot(driver:webdriver.Chrome):
    try:
        driver.find_element(By.XPATH,"//div[@class='crossIcon chatBot chatBot-ic-cross']").click()
        logwriter(f"chatbot closed")
    except:
        driver.find_element(By.TAG_NAME,'body').click()


def login(email:str,password:str):
    #Setting arguments
    option=Options()
    option.add_argument(fr'--user-data-dir={userdir}')
    option.add_argument(argument='--headless')    
    option.add_argument(argument='user-agent=Mozilla/5.0 '+
    '(iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '+
    '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')

    driver=webdriver.Chrome(executable_path='chromedriver.exe',options=option)
    driver.get("https://www.naukri.com/mnj/login?")
    driver.set_window_size(360,740) #emulate as mobile
    driver.implicitly_wait(10)
    #Sending inputs
    try:
        driver.find_element(By.ID,value='usernameField').send_keys(email)
        driver.find_element(By.ID,value='passwordField').send_keys(password)
    except:
        inp=input("You are logged in already\nWant to clear previous login credential? Y or N\n")
        if inp.lower() == 'y' or inp.lower() in 'yes':
            driver.quit()
            shutil.rmtree('userdata')
            input("Credential cleared\nLogin again\nenter to continue")
            sys.exit() 
        else:
            driver.quit()
            sys.exit()
    driver.implicitly_wait(20)
    try:
        driver.find_element(By.XPATH,value="//div[@class='action']"+
                        "/button[@data-ga-track='NormalLogin|Login']").click()
        input("Login succeeded.\npress enter")
        driver.quit()
    except ex.ElementClickInterceptedException:
        input("Please login manually\npress enter to continue")
        option=Options()
        option.add_argument(fr'--user-data-dir={userdir}')
        driver=webdriver.Chrome(executable_path='chromedriver.exe',options=option)
        driver.get("https://www.naukri.com/nlogin/login")
        driver.execute_script('alert("Proceed login, Dont close the browser\nGo back to console")')
        input("Are you logged in?\npress enter")
        driver.quit()
    except:
        print("Unexpected error\n trying to loggin....")
        driver.quit()
        login(email,password)
    logwriter("Login success")


def setjoburl():
    '''Interactable browser to set filter for job'''
    option=Options()
    option.add_argument(fr'--user-data-dir={userdir}')
    driver=webdriver.Chrome(executable_path='chromedriver.exe',options=option)
    driver.get("https://www.naukri.com/mnjuser/homepage")
    driver.maximize_window()
    try:
        driver.find_element(By.XPATH,"//button[@class='nI-gNb-sb__icon-wrapper']").click()
    except:
        close_chatbot(driver)
        driver.find_element(By.XPATH,"//button[@class='nI-gNb-sb__icon-wrapper']").click()    
    driver.execute_script('alert("Set filter and go back to console")')
    input("press enter if you finished job filltering")
    jobspage=driver.current_url
    driver.quit()#browser closed
    with open(qlfile,'w')as file:
        data=json.dumps(jobspage)
        file.write(data)
    logwriter('Filtered job query link captured')
    print('Filtered job query link captured')


def applyjobs(filteredjobs:str,applylimit:int=10):
    option=Options()
    option.add_argument(argument='--headless')    
    option.add_argument(fr'--user-data-dir={userdir}')
    option.add_argument(argument='user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '+
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    driver=webdriver.Chrome(executable_path='chromedriver.exe',options=option)
    driver.get(filteredjobs)
    driver.implicitly_wait(20)
    jobcount=driver.find_element(By.XPATH,"//span[@class='fleft grey-text mr-5 fs12']").text
    jobcount=jobcount[jobcount.find("of")+3:]
    print(jobcount)
    increval=1
    successrate=0
    windows=driver.window_handles
    while successrate < applylimit:
        driver.switch_to.window(windows[0])#Job Listing window
        driver.find_element(By.XPATH,f"//div[@class='list']/article[{increval}]").click()
        increval+=1
        windows=driver.window_handles
        driver.switch_to.window(windows[1])
        try:
            driver.find_element(By.ID,"//span[@class='already-applied']")
            driver.execute_script('close()')
            continue
        except:
            pass#dummy pass  
        try:
            driver.find_element(By.XPATH,"//button[@class='waves-effect waves-ripple btn apply-button']").click()
        except:
            logwriter("Apply on site error")
            driver.execute_script('close()')
            continue
        try:
            #close prompting window
            driver.find_element(By.ID,'skip_qup').click()
        except:
            try:
                driver.find_element(By.ID,'closeLB').click()
                driver.execute_script('close()')
                continue
            except:
                pass
        url=driver.current_url
        driver.implicitly_wait(30)
        try:
            status=driver.find_element(By.XPATH,"//div[@class='upper-section']/span[@class='apply-message']").text
            successrate+=1
            logwriter(f"{status}\n{url}")
            driver.execute_script('close()')
        except:
            logwriter("Apply message not found")
            driver.execute_script('close()')
            continue
    driver.quit()
    logwriter(f"success ratio {successrate}/{applylimit}")


def browserinspect():
    option=Options()
    #option.add_argument(argument='--headless')    
    option.add_argument(fr'--user-data-dir={userdir}')
    driver=webdriver.Chrome(executable_path='chromedriver.exe',options=option)
    driver.get('https://www.naukri.com/')
    input("press enter to stop")