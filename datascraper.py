from selenium import webdriver
import pyrebase
import requests
import time
import os
from selenium.webdriver.chrome.options import Options


#Initialize database
config = {
    "apiKey": "AIzaSyAPA5LfWoIJBwc9n5MyAAtx7g2pAdsKw18y",
    "authDomain": "gtvolleyball-68352.firebaseapp.com",
    "storageBucket": "gtvolleyball-68352.appspot.com",
    "databaseURL": "https://gtvolleyball-68352.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#Open webpage on safari


chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
browser.get("http://app.myvert.com/coach/events")
username = browser.find_element_by_id('user_email')
password = browser.find_element_by_id('user_password')
submit = browser.find_element_by_name("commit")

#Login to webpage
username.send_keys("mcollier@athletics.gatech.edu")
password.send_keys("gtvolleyball2018")
print("exec1")
submit.submit()

#Wait until page loads
time.sleep(5)

#Temporarily transfer the first 20 items
tempStart = 6
tempEnd = 20

ref = browser.find_elements_by_xpath("//body/div[2]/div/div/div/table/tbody")
print(ref[0].find_elements_by_xpath('tr')[6])
"""
hyperlink = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[0].text
event = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[7].text
date = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[8].text

for i in range(tempStart, tempEnd):

    #Get the hyperlink, date, and event id reference
    print(browser.page_source)
    ref = browser.find_elements_by_xpath("//body/div[2]/div/div/div/table/tbody")
    hyperlink = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[0].text
    event = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[7].text
    date = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[8].text

    #Make event json parsable
    for letter in event:
        if letter == "/":
            event = event.replace(letter,"-")

    print('exec2')
    #Wait until page loads
    time.sleep(5)

    #Open the new page with the event id
    url = "http://app.myvert.com/coach/events/" + hyperlink
    browser.get(url)

    #Wait until page loads
    time.sleep(5)

    #Request data from the json url
    data = browser.find_elements_by_xpath("//body/div[2]/div[2]/div[2]/div[3]/div/div/tt/a")
    print(data)
    r = requests.get(data[0].get_attribute("href"))
    print(r.json())

    #Push the data to firebase
    #db.child(event).child(date).update(r.json())

    #Go back to home page
    #browser.get("http://app.myvert.com/coach/events")

    #Wait until page loads
    #time.sleep(5)"""

browser.quit()