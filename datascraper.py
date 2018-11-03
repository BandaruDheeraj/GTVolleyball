from selenium import webdriver
import pyrebase
import requests

import time

browser = webdriver.Safari()
browser.get("http://app.myvert.com/coach/events")
username = browser.find_element_by_id('user_email')
password = browser.find_element_by_id('user_password')
submit = browser.find_element_by_name("commit")

username.send_keys("mcollier@athletics.gatech.edu")
password.send_keys("gtvolleyball2018")
submit.submit()
time.sleep(10)



for i in range(0, 20):
    ref = browser.find_elements_by_xpath("//body/div[2]/div/div/div/table/tbody")
    hyperlink = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[0].text
    print(hyperlink)
    time.sleep(5)
    url = "http://app.myvert.com/coach/events/" + hyperlink
    browser.get(url)
    time.sleep(5)
    data = browser.find_elements_by_xpath("//body/div[2]/div[2]/div[2]/div[3]/div/div/tt/a")
    r = requests.get(data[0].get_attribute("href"))
    print(r.json())
    browser.get("http://app.myvert.com/coach/events")
    time.sleep(5)

browser.quit()