import threading
import os
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import keyboard

load_dotenv()

EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('SENHA')

running = True

def run_script():
    global running
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    chromedriver_path = ChromeDriverManager().install()
    if 'THIRD_PARTY_NOTICES.chromedriver' in chromedriver_path:
        chromedriver_path = chromedriver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver.exe')
    
    chrome_service = ChromeService(chromedriver_path)
    navegador = webdriver.Chrome(service=chrome_service, options=chrome_options)

    navegador.get("https://app.climberrms.com/login")
    navegador.fullscreen_window()
    navegador.execute_script("document.body.style.zoom='75%'")

    navegador.find_element(By.XPATH, '/html/body/jhi-main/climber-login/div[2]/div/jhi-login-modal/form/div[1]/input').send_keys(EMAIL)
    navegador.find_element(By.XPATH, '/html/body/jhi-main/climber-login/div[2]/div/jhi-login-modal/form/div[2]/input').send_keys(SENHA)
    navegador.find_element(By.XPATH, '/html/body/jhi-main/climber-login/div[2]/div/jhi-login-modal/form/button').submit()
    sleep(3)

    while running:
        dropdown_items = navegador.find_elements(By.XPATH, '/html/body/jhi-main/climber-shell/climber-header/nav[2]/div/div[2]/climber-dropdown-v2/div[2]/div/div[2]/div')
        num_items = len(dropdown_items)

        for num in range(1, num_items + 1):
            if not running:
                break
            dropdown = navegador.find_element(By.XPATH, '/html/body/jhi-main/climber-shell/climber-header/nav[2]/div/div[2]/climber-dropdown-v2/div[1]/div/div')
            navegador.execute_script("arguments[0].click();", dropdown)
            hotel = navegador.find_element(By.XPATH, f'/html/body/jhi-main/climber-shell/climber-header/nav[2]/div/div[2]/climber-dropdown-v2/div[2]/div/div[2]/div[{num}]')
            navegador.execute_script("arguments[0].click();", hotel)
            sleep(10)

    navegador.quit()

def stop_script():
    global running
    running = False

keyboard.add_hotkey('ctrl+3', stop_script)

script_thread = threading.Thread(target=run_script)
script_thread.start()

keyboard.wait('ctrl+3')
script_thread.join()