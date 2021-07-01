# !/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time

FLAGS = ['Google', 'Ctrip', 'Qunar', 'Fliggy']
chrome_driver_path = os.path.join('widget', 'chromedriver.exe')

def crawl_start(flag, input_date):
    global driver
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('lang=zh_CN.UTF-8')
    # options.add_argument('user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
    options.add_argument('--disable-infobars')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--incognito')
    options.add_argument('window-size=1920x3000')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(chrome_driver_path, options=options)
    
        
    if flag == 'Ctrip':
        url = f'https://flights.ctrip.com/international/search/oneway-hkg-hou?depdate={input_date}&cabin=y_s&adult=1&child=0&infant=0&searchid=j1047145171-1625058867135-12470Ae-0'
        driver.get(url)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="outerContainer"]/div/div[3]/div/a').click()
        time.sleep(10)
        full_page = driver.page_source
        soup = BeautifulSoup(full_page, 'html5lib')
        # flight_items = etree.HTML(str(soup)).xpath('//*[@id="app"]/div/div[3]/div[3]/div[2]/span/div/div[1]/div/div/div')
        flight_items = soup.find_all('div', class_='flight-item')
        # flight_items = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "flight-item active")))
        # flight_items = driver.find_element_by_xpath('//div[contains(@class, "flight-item")]')
        # flight_items = driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[3]/div[2]/span/div/div[1]/div/div/div')
        # items_html = flight_items.get_attribute('innerHTML')
        # items_display = flight_items.is_displayed()
        # print(items_display)
        # flight_items = list(flight_items)
        # print(input_date, len(items_html))
        # print(full_page)
        print(len(flight_items))
        driver.close()
        return flight_items
    
    """
    if flag == 'Google':
        conn = sqlite3.connect(os.path.join('database', 'google_flight.db'))
        cur = conn.cursor()
        cur.execute("SELECT url FROM google_flight WHERE date = ?", (input_date, ))
        url = cur.fetchone()[0]
        cur.close()
        conn.commit()
        conn.close()
        driver.get(url)
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # content = soup.select('div[class="KC3CM"]')
        # print(content)
        print(driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div/c-wiz/div[2]/div[3]/div/div[2]/div[4]/div/div[2]/div/div[1]/div'))
    """
    
# crawl_start('Ctrip', '2021-08-20')





def flight_info_render(input_date):
    [input_year, input_month, input_day] = str(input_date).split('-')


