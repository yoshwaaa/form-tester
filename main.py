import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from pagesMG import pages

driver = webdriver.Chrome('/usr/local/bin/chromedriver')

# loop through the pages
for page in pages:
    driver.get(page)
    if driver.find_element_by_class_name('accordion-btn-next'):
      try:
        diagnosis = driver.find_element_by_name("diagnosis")
        diagnosis.send_keys("u")
        diagnosis.send_keys(Keys.RETURN)
      except:
          pass

      try:
          clickNext = driver.find_element_by_class_name('accordion-btn-next')
          clickNext.click()
      except:
          pass

      time.sleep(1)

      try:
          name = driver.find_element_by_name("full_name")
          name.send_keys("Automated Form Test")
      except:
          pass

      try:
          email = driver.find_element_by_name("email_address")
          email.send_keys("automated@formtest.com")
      except:
          pass

      try:
          phone = driver.find_element_by_name("phone_number")
          phone.send_keys("4073250884")
      except:
          pass

      time.sleep(5)
      
    else:
    
      try:
          name = driver.find_element_by_name("full_name")
          name.send_keys("Automated Form Test")
      except:
          pass

      try:
          email = driver.find_element_by_name("email_address")
          email.send_keys("automated@formtest.com")
      except:
          pass

      try:
          phone = driver.find_element_by_name("phone_number")
          phone.send_keys("4073250884")
      except:
          pass

      try:
          diagnosis = driver.find_element_by_name("diagnosis")
          diagnosis.send_keys("u")
          diagnosis.send_keys(Keys.RETURN)
      except:
          pass

      try:
          address = driver.find_element_by_name("user_address")
          address.send_keys("555 Automated Test")
      except:
          pass

      try:
          city = driver.find_element_by_name("user_city")
          city.send_keys("Automation")
      except:
          pass

      try:
          state = driver.find_element_by_name("user_state")
          state.send_keys("KS")
          state.send_keys(Keys.RETURN)
      except:
          pass

      try:
          user_zip = driver.find_element_by_name("user_zip")
          user_zip.send_keys("66213")
      except:
          pass

      try:
          message =  driver.find_element_by_name("message")
          message.send_keys("This form test should only go to Josh.  If lost, please return to joshua.lohse@mesotheliomaguide.com")
      except:
          pass

          # submit the form!!
      try:
          submit = driver.find_element_by_name("submitConversionForm")
          submit.send_keys(Keys.RETURN)
      except:
          pass

      time.sleep(5)
      try:
          driver.find_element_by_class_name('success')
      except:
          pass

driver.quit()

print('Good job dude, your script ran without error')
