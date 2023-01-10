import csv
import os
from pathlib import Path
from typing import List
from time import sleep

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from _backend import send_messanger, send_email_attachment, insert, query

website = 'http://www.azair.eu'

def get_web_driver():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(width=1200, height=1000)

    driver.get(website)
    return driver

def data_month_parser(date):
    split = date.split('-')
    return split[0] + split[1]


def data_day_parser(date):
    split = date.split('-')
    day = None
    if(split[2][0] == '0'):
        day = split[2][1]
    else :
        day = split[2]
    return day

def set_data(driver, date_1, date_2):
    table = []
    date = ""
    for k in range(1, 3):
        if (k == 1):
            table = "depmonth"
            date = date_1
        else:
            table = "arrmonth"
            date = date_2
        set_month = driver.find_element("name", table)  # arrdate
        dd = Select(set_month)
        try:
            dd.select_by_value(data_month_parser(date))
        except:
            pass

        try:
            for i in range(3, 9):
                for j in range(1, 8):
                    path = f'//*[@id="nonflexiCal"]/div[1]/div[{k}]/table/tbody/tr[{i}]/td[{j}]'
                    if (driver.find_element(By.XPATH, path).text == data_day_parser(date)):
                        driver.find_element(By.XPATH,
                                            path).click()
        except:
            for i in range(3, 8):
                for j in range(1, 8):
                    path = f'//*[@id="nonflexiCal"]/div[1]/div[{k}]/table/tbody/tr[{i}]/td[{j}]'
                    if (driver.find_element(By.XPATH, path).text == data_day_parser(date)):
                        driver.find_element(By.XPATH,
                                            path).click()
        sleep(0.2)



def range_days(driver, min_days, max_days):
    driver.find_element(By.XPATH, "//*[@id='minDaysStay']").clear()
    driver.find_element(By.XPATH, "//*[@id='maxDaysStay']").clear()
    driver.find_element(By.XPATH, "//*[@id='minDaysStay']").send_keys(min_days)
    driver.find_element(By.XPATH, "//*[@id='maxDaysStay']").send_keys(max_days)


def set_pln(driver):
    driver.find_element("name", "currency").click()
    driver.find_element(By.XPATH, "/html/body/div[4]/form/div[4]/span[4]/select/option[3]").click()

def read_csv_file(input_file: str) -> List[List[str]]:
    # list comprehension
    return [row for row in
            csv.reader(Path(input_file).read_text(
                encoding="utf-8").splitlines(),
                       delimiter=',')][1:]

def click_search(driver):
    search = driver.find_element("name", "indexSubmit")
    try:
        for x in range(3):
            search.click()
            sleep(0.2)
    except:
        pass
        # print("Click exception")


def change_place(driver, box, place_to_replace, new_place, data, n):
    driver.execute_script("arguments[0].value = ''", box)
    box.send_keys(Keys.ARROW_DOWN)
    driver.execute_script("arguments[0].value = ''", box)

    box.send_keys(new_place)
    box.send_keys(Keys.ARROW_DOWN)
    box.send_keys(Keys.RETURN)

    data_from_box_scrapped = driver.find_element(By.XPATH, '*//input[@name="srcAirport"]').get_attribute(
        'value')
    data_to_box_scrapped = driver.find_element(By.XPATH, '*//input[@name="dstAirport"]').get_attribute('value')

    iata_code = lambda str: (str[str.find("[") + 1:str.find("]")]).split() + (
        str[str.find("+") + 1:str.find(")")]).split(',')
    place = lambda str: (str[str.find(""):str.find("[") - 1])

    data[8] = (iata_code(data_from_box_scrapped))
    data[9] = (iata_code(data_to_box_scrapped))

    df = pd.read_csv("D:/programownie funkcyjne/final_project/_gui/1.csv")

    if(n == 1):
        df.replace(place_to_replace, place(data_from_box_scrapped), inplace=True)
    else:
        df.replace(place_to_replace, place(data_to_box_scrapped), inplace=True)

    df.to_csv("D:/programownie funkcyjne/final_project/_gui/1.csv", index=False)




def from_to(driver, data):
    place_start = data[1]
    place_finish = data[2]


    from_box = driver.find_element("name", "srcAirport")

    driver.execute_script("arguments[0].value = ''", from_box)
    from_box.send_keys(Keys.ARROW_DOWN)
    driver.execute_script("arguments[0].value = ''", from_box)

    from_box.send_keys(place_start)
    from_box.send_keys(Keys.ARROW_DOWN)
    from_box.send_keys(Keys.RETURN)

    to_box = driver.find_element("name", "dstAirport")

    driver.execute_script("arguments[0].value = ''", to_box)
    to_box.send_keys(Keys.ARROW_DOWN)
    driver.execute_script("arguments[0].value = ''", to_box)

    to_box.send_keys(place_finish)
    to_box.send_keys(Keys.ARROW_DOWN)
    to_box.send_keys(Keys.RETURN)

    data_from_box_scrapped = driver.find_element(By.XPATH, '*//input[@name="srcAirport"]').get_attribute('value')
    data_to_box_scrapped = driver.find_element(By.XPATH, '*//input[@name="dstAirport"]').get_attribute('value')

    iata_code = lambda str: (str[str.find("[") + 1:str.find("]")]).split() + (
    str[str.find("+") + 1:str.find(")")]).split(',')
    place = lambda str : (str[str.find(""):str.find("[") -1])


    data.append(iata_code(data_from_box_scrapped))
    data.append(iata_code(data_to_box_scrapped))

    click_search(driver)

    try:

        if(driver.find_element(By.XPATH, '// *[ @ id = "srcErrCaption"]').text == 'AIRPORT DOES NOT EXIST'):
            change_place(driver, from_box, data[1], "Warsaw", data, 1)
            click_search(driver)
    except:
        pass
        # print("Blad 1")

    try:
        if (driver.find_element(By.XPATH, '// *[ @ id = "dstErrCaption"]').text == 'AIRPORT DOES NOT EXIST'):
            change_place(driver, to_box, data[2], "Italy", data, 2)
            click_search(driver)
    except:
        pass
        # print("Blad 2")



def scrap(driver):
    date_dep_to_dest = list(
        map(lambda x: datetime.strptime(x.text.split(' ')[1], "%d/%m/%y"), driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/p[1]/span[2]')))
    hour_dep_to_dest = list(
        map(lambda x: x.text, driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/p[1]/span[3]')))
    hour_arr_to_dest = list(
        map(lambda x: x.text, driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/p[1]/span[4]')))
    flight_time_to_dest = list(
        map(lambda x: x.text, driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/p[1]/span[5]')))


    date_dep_from_dest = list(
        map(lambda x: datetime.strptime(x.text.split(' ')[1], "%d/%m/%y"), driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/p[2]/span[2]')))
    hour_dep_from_dest = list(
        map(lambda x: x.text, driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/p[2]/span[3]')))
    hour_arr_from_dest = list(
        map(lambda x: x.text, driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/p[2]/span[4]')))
    flight_time_from_dest = list(
        map(lambda x: x.text, driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/p[2]/span[5]')))


    total_prize = list(
        map(lambda x: x.text, driver.find_elements(By.XPATH, '//div[@class="result "]/div[1]/div[6]/span[1]')))
    url = list(
        map(lambda x: x.get_attribute('href'), driver.find_elements(By.XPATH, '//div[@class="result "]/div[2]/a')))


    final1 = list(
        zip(date_dep_to_dest,
            hour_dep_to_dest,
            hour_arr_to_dest,
            flight_time_to_dest,
            date_dep_from_dest,
            hour_dep_from_dest,
            hour_arr_from_dest,
            flight_time_from_dest,
            total_prize,
            url
    ))
    insert.insertF(final1)
    driver.get(website)
    set_pln(driver)



def start():
    driver = get_web_driver()
    input = read_csv_file("D:/programownie funkcyjne/final_project/_gui/1.csv")
    query.delete_old_rows()
    set_pln(driver)
    for data in input:
        set_data(driver, data[3], data[4])
        range_days(driver, data[5], data[6])
        from_to(driver, data)
        scrap(driver)
        query.complicant_data_to_file(data)
        if(os.path.exists('flights.txt')):
            send_email_attachment.execute()
            send_messanger.execute()
            os.remove('flights.txt')








