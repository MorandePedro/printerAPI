from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import IPython

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--silent")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-web-security")
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

def getParams(ip):
    navegador = webdriver.Chrome(options=options)
    wait = WebDriverWait(navegador, 10)
    
    navegador.get(f"http://{ip}")

    if not 'brother' in navegador.page_source.lower():
        
        if 'spa_login.html' in navegador.current_url:
            
            iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            navegador.switch_to.frame(iframe)
            wait.until(EC.presence_of_element_located((By.ID,'ID_LGI_LOGIN_BT'))).click()
            navegador.switch_to.default_content()
        
        
        click_with_js(navegador, By.ID, 'ID_Menu_System')
        click_with_js(navegador, By.ID, 'ID_SubMenu_System_DeviceInfo')
        click_with_js(navegador, By.ID, 'ID_SpareSubMenu_System_DeviceStatus')

        log_msg = wait_for_log(navegador, "_111_000_INF000?_")

        if log_msg:
            log_json = json.loads(log_msg)["message"]["params"]["request"]
            url = log_json['url'].split('?')[0]
            header = log_json['headers']
            cookies = {}
            for val in navegador.get_cookies():
                cookies[val['name']] = val['value']
    
        counter = {}

        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        navegador.switch_to.frame(iframe)
        counter['SerialNumber'] = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ID_INF_0"]/div/div[3]/table/tbody/tr[4]/td'))).text
        
        navegador.switch_to.default_content()
        wait.until(EC.presence_of_element_located((By.ID,'ID_SpareSubMenu_System_Counter'))).click()

        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        navegador.switch_to.frame(iframe)

        counter['Mono'] = int(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="cms_grid_6_0"]/div/div/table/tbody/tr[2]/td'))).text)
        counter['Color'] = int(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ID_TR_Color"]/td'))).text)    
        counter['Total'] = counter['Mono'] + counter['Color']

        navegador.switch_to.default_content()
        navegador.quit()
        
        return {'Header': header, 'Cookies': cookies, 'Url': url, 'Counter': counter, 'Brand': 'Konica'}
    else:
        try:
            wait.until(EC.presence_of_element_located((By.ID,'ChangeToHTTPSButton'))).click()
            wait.until(EC.presence_of_element_located((By.ID,'LogBox'))).click()
            wait.until(EC.presence_of_element_located((By.ID,'LogBox'))).send_keys("@Bbr92729272")
            wait.until(EC.presence_of_element_located((By.ID,'login'))).click()            

            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="menu_tree_root"]/div[2]/a'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="general_sub"]/div[1]/a'))).click()

            toner = int(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pageContents"]/form/div[7]/dl/dd[10]'))).text.split('%')[0])

            serial = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pageContents"]/form/div[5]/dl/dd[2]'))).text

            drumUnit = int(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pageContents"]/form/div[7]/dl/dd[1]'))).text.split('%')[0])

            counter = int(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pageContents"]/form/div[10]/dl/dd[1]'))).text.split('Page')[0])

            output = {
                'Brand': 'Brother',
                'Status': 'Online',
                'IP': ip,
                'Counter': {
                    'Mono': counter,
                    'Color': 0,
                    'Total': counter,
                    'SerialNumber': serial
                },
                'Toner': [
                    {
                    "Name": "Toner (Yellow)",
                    "Percent": 0,
                    "State": "-"
                    },
                    {
                    "Name": "Toner (Magent)",
                    "Percent": 0,
                    "State": "-"
                    },
                    {
                    "Name": "Toner (Cyan)",
                    "Percent": 0,
                    "State": "-"
                    },
                    {
                    "Name": "Toner (Black)",
                    "Percent": toner,
                    "State": "-"
                    }
                ],
                'ImagingUnit': [
                    {
                    "Name": "Imaging Unit (Yellow)",
                    "Percent": 0,
                    "State": "-"
                    },
                    {
                    "Name": "Imaging Unit (Magenta)",
                    "Percent": 0,
                    "State": "-"
                    },
                    {
                    "Name": "Imaging Unit (Cyan)",
                    "Percent": 0,
                    "State": "-"
                    },
                    {
                    "Name": "Imaging Unit (Black)",
                    "Percent": drumUnit,
                    "State": "-"
                    }
                ]
            }
            return(output)
        except:
            return {'Status': 'Offline', 'IP': ip, 'Brand': 'Brother'}

def click_with_js(driver, by, value):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
    driver.execute_script("arguments[0].click();", element)

def wait_for_log(driver, search_string, timeout=10, interval=0.2):
    start_time = time.time()
    while time.time() - start_time < timeout:
        logs = driver.get_log("performance") 
        for entry in logs:
            log_msg = entry["message"]
            if search_string in log_msg:
                return log_msg
        time.sleep(interval)
    return False