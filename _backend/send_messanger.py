from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_web_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(width=1200, height=1000)
    website = 'https://www.messenger.com/login/'
    driver.get(website)
    sleep(0.5)
    return  driver

login = ''
password = ''
people = ['Marek Kowalski','Janek Bitkowski']
message = f'Pojawił sie nowy lot. Sprawdz email'

def login(driver):
    driver.find_elements(By.XPATH, "//button[contains(string(), 'Zezwól na korzystanie z niezbędnych i opcjonalnych plików cookie')]")[0].click()
    sleep(0.2)
    driver.find_element(By.XPATH, "//*[@id='email']").send_keys('jujoma903@gmail.com')
    sleep(0.2)
    driver.find_element(By.XPATH, "//*[@id='pass']").send_keys(password)
    sleep(0.2)
    driver.find_element(By.XPATH, "//*[@id='loginbutton']").click()
    sleep(4)

def send_message(driver):
    for person in people:

        path1 = f"// input[@value='{person}']"
        path2 = f"// input[@value='Wyszukaj zapytanie „{person}” w wiadomościach']"
        path3 = f"// input[@value='{person}']"
        driver.find_element(By.XPATH, "// input[@value='']").send_keys(person)
        sleep(0.2)
        driver.find_element(By.XPATH, path1).send_keys(Keys.ARROW_DOWN)
        sleep(0.2)
        driver.find_element(By.XPATH, path2).send_keys(Keys.ARROW_DOWN)
        sleep(0.2)
        driver.find_element(By.XPATH, path3).send_keys(Keys.ENTER)
        sleep(0.2)
        textbox = driver.switch_to.active_element
        sleep(0.2)
        textbox.send_keys(message)
        sleep(0.2)
        textbox.send_keys(Keys.ENTER)


def execute():
    driver = get_web_driver()
    login(driver)
    send_message(driver)






