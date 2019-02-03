from selenium import webdriver
import pyrebase
import requests
import time

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
browser = webdriver.Chrome()
browser.get("http://app.myvert.com/coach/events")
username = browser.find_element_by_id('user_email')
password = browser.find_element_by_id('user_password')
submit = browser.find_element_by_name("commit")

#Login to webpage
username.send_keys("mcollier@athletics.gatech.edu")
password.send_keys("gtvolleyball2018")
submit.submit()

#Wait until page loads
time.sleep(5)

#Temporarily transfer the first 20 items
tempStart = 0
tempEnd = 20
for i in range(tempStart, tempEnd):

    #Get the hyperlink, date, and event id reference
    ref = browser.find_elements_by_xpath("//body/div[2]/div/div/div/table/tbody")
    hyperlink = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[0].text
    event = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[7].text
    date = ref[0].find_elements_by_xpath("tr")[i].find_elements_by_xpath("td")[8].text

    #Make event json parsable
    for letter in event:
        if letter == "/":
            event = event.replace(letter,"-")

    #Wait until page loads
    time.sleep(5)

    #Open the new page with the event id
    url = "http://app.myvert.com/coach/events/" + hyperlink
    browser.get(url)

    #Wait until page loads
    time.sleep(5)

    #Request data from the json url
    data = browser.find_elements_by_xpath("//body/div[2]/div[2]/div[2]/div[3]/div/div/tt/a")
    r = requests.get(data[0].get_attribute("href"))

    #Push the data to firebase
    db.child(event).child(date).update(r.json())

    #Go back to home page
    browser.get("http://app.myvert.com/coach/events")

    #Wait until page loads
    time.sleep(5)

browser.quit()