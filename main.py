from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep, time
#import dns.resolver #dnspython
import requests
import concurrent.futures
from dotenv import dotenv_values

start = time()
exit_code = 1
return_code = "1: Did nothing,"

def getData(data:str)->str:
    config = dotenv_values(".env")
    try:
        if data in config and config[data] != None:
            return config[data]
    except:
        raise ValueError("Invalid key or empty value.")
        return ''

def fetch_url(url:str)->str:
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return url
        else:
            return ''
    except requests.RequestException:
        return ''

def check_urls(urls:list[str])->str:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result!='':
                for f in futures:
                    if f != future:
                        f.cancel()
                return result
    raise RuntimeError
    return ''


def getUrl()->str:
    hostel_url = 'https://iach.srmist.edu.in/Connect/'
    ub_url = 'https://iac.srmist.edu.in/Connect/'
    urls = [hostel_url, ub_url]
    return check_urls(urls)

driver = webdriver.Chrome()

login_selector = "LoginUserPassword_auth_username"
pass_selector  = "LoginUserPassword_auth_password"
button_selector = "UserCheck_Login_Button_span"


try:
    driver.get(getUrl())
    driver.implicitly_wait(3)
    login_element = driver.find_element(By.ID, login_selector)
    pass_element = driver.find_element(By.ID, pass_selector)
    login_element.send_keys(getData("username"))
    pass_element.send_keys(getData("password"))
    button = driver.find_element(By.ID, button_selector)
    button.click()
    return_code = "0: Logged in"
    exit_code = 0
except RuntimeError:
    return_code = "1: Not on SRMIST"
    exit_code = 1
except Exception as e:
    print(e)
    return_code = "0: Already logged in."
    exit_code = 0
finally:
    print(return_code)
    sleep(1)
    driver.quit()
    print(f"Took {time()-start:.2f} seconds to complete login.")
    exit(exit_code)
