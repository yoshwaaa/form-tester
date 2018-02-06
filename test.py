import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import InvalidElementStateException
import string
from random import randint
import random
import requests
from time import strftime
from lxml import html
from lxml.cssselect import CSSSelector
import sys

from pagesMG import static_pages
from get_phone import get_phone
from db import db_connect

def get_links(static_pages):
    sitemaps = ['https://www.mesotheliomaguide.com/doctors-sitemap.xml', 'https://www.mesotheliomaguide.com/cancer-centers-sitemap.xml', 'https://www.mesotheliomaguide.com/post-sitemap.xml', 'https://www.mesotheliomaguide.com/page-sitemap.xml']

    sitemap_links = []
    raw_list = []
    img_ext = ['jpg', 'jpeg', 'png', 'gif']
    for sitemap in sitemaps:
        page = requests.get(sitemap)
        tree = html.fromstring(page.content)
        tree_tc = tree.text_content()
        tree_repl = tree_tc.replace('\t', '')
        tree_list = tree_repl.split('\n')

        raw_list.append(tree_list)

    flat_list = sum(raw_list, [])
    for rl in flat_list:
        if not rl:
            continue
        elif 'jpg' in rl:
            continue
        elif 'png' in rl:
            continue
        elif 'jpeg' in rl:
            continue
        elif 'gif' in rl:
            continue

        if 'https' in rl:
            sitemap_links.append(rl)

    total_links = sitemap_links + static_pages
    total_links = list(set(total_links))

    return total_links

def fillout_form(driver, form_input, fail_count):
    try:
        name = driver.find_element_by_name("full_name")
        name.send_keys(form_input['name'])
    except(NoSuchElementException):
        pass

    try:
        email = driver.find_element_by_name("email_address")
        email.send_keys(form_input['email'])
    except(NoSuchElementException):
        pass

    try:
        phone = driver.find_element_by_name("phone_number")
        phone.send_keys(form_input['phone'])
    except(NoSuchElementException):
        pass

    try:
        diagnosis = driver.find_element_by_name("diagnosis")
        diagnosis.send_keys("u")
        diagnosis.send_keys(Keys.RETURN)
    except(NoSuchElementException):
        pass

    try:
        address = driver.find_element_by_name("user_address")
        address.send_keys(form_input['address'])
    except(NoSuchElementException):
        pass

    try:
        city = driver.find_element_by_name("user_city")
        city.send_keys(form_input['city'])
    except(NoSuchElementException):
        pass

    try:
        state = driver.find_element_by_name("user_state")
        state.send_keys(form_input['state'])
        state.send_keys(Keys.RETURN)
    except(NoSuchElementException):
        pass

    try:
        user_zip = driver.find_element_by_name("user_zip")
        user_zip.send_keys(form_input['user_zip'])
    except(NoSuchElementException):
        pass

    try:
        message =  driver.find_element_by_name("body_message")
        message.send_keys(form_input['message'])
    except(NoSuchElementException):
        pass

    # submit on the name input
    try:
        name.send_keys(Keys.RETURN)
    except(NoSuchElementException):
        pass

    try:
        driver.find_element_by_class_name('success')
        return True
    except(NoSuchElementException):
        return False

def page_has_form(driver):
    try:
        driver.find_element_by_class_name('form')
        driver.find_element_by_name('submitConversionForm')
        return True
    except(NoSuchElementException, ElementNotVisibleException):
        return False

def generate_form_input(phone):
    form_inputs = {}
    form_fields = ['name', 'phone', 'diagnosis', 'address', 'city', 'state', 'user_zip', 'message']
    for form_field in form_fields:
        if form_field == 'name':
            form_inputs['name'] = 'Automated Form Test v2'
        elif form_field == 'phone':
            f = open('phone_numbers', 'r')
            phone_numbers = f.readlines()
            phone = phone_numbers[randint(0,len(phone_numbers)-1)].strip('\n')
            form_inputs['phone'] = phone

        elif form_field == 'diagnosis':
            form_inputs['diagnosis'] = 'unknown'

        elif form_field == 'address':
            num_len = randint(1,10)
            name_len = randint(5,15)

            street_num = ''
            for i in range(num_len):
                street_num = street_num + random.choice(string.digits)

            street_name = ''
            for i in range(name_len):
                street_name = street_name + random.choice(string.ascii_lowercase)

            address = street_num + ' ' + street_name

            form_inputs['address'] = address

        elif form_field == 'city':
            city_len = randint(3,15)

            city_name = ''
            for i in range(city_len):
                city_name = city_name + random.choice(string.ascii_lowercase)

            form_inputs['city'] = city_name

        elif form_field == 'state':
            states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                      "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                      "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                      "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                      "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
            state = random.choice(states)

            form_inputs['state'] = state

        elif form_field == 'user_zip':
            user_zip = ''
            for i in range(5):
                user_zip = user_zip + random.choice(string.digits)

            form_inputs['user_zip'] = user_zip

        elif form_field == 'message':
            msg_len = randint(20,150)

            message = ''
            choice = string.digits + " " + string.ascii_lowercase
            for i in range(msg_len):
                message = message + random.choice(choice)

            form_inputs['message'] = message

        form_inputs['referral_link'] = driver.current_url

    return form_inputs

def insert_into_sent_forms_and_sent_received(conn, form_input):
    cur = conn.cursor()
    cur.execute("INSERT INTO sent_forms (name, phone, diagnosis, address, city, state, zip, message, referral_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;", [form_input['name'], form_input['phone'], form_input['diagnosis'], form_input['address'], form_input['city'], form_input['state'], form_input['user_zip'], form_input['message'], form_input['referral_link']])
    sent_forms_id = cur.fetchone()[0]
    conn.commit()
    cur.close()

    cur = conn.cursor()
    cur.execute("INSERT INTO sent_received (sent_id) VALUES (%s) RETURNING id;", [sent_forms_id])
    sent_received_id = cur.fetchone()[0]
    conn.commit()
    cur.close()

    return sent_forms_id, sent_received_id

def reset_email_in_form_input(form_input, sent_received_id):
    form_input['email'] = str(sent_received_id) + '@uid.com'
    return form_input

def update_sent_forms_with_email(conn, sent_forms_id, form_input):
    cur = conn.cursor()
    cur.execute("UPDATE sent_forms SET email = %s  WHERE id = %s;", [form_input['email'], sent_forms_id])
    conn.commit()
    cur.close()

def update_sent_forms_with_sent_flag(conn, sent_forms_id, sent_flag):
    cur = conn.cursor()
    cur.execute("UPDATE sent_forms SET sent_flag = %s  WHERE id = %s;", [sent_flag, sent_forms_id])
    conn.commit()
    cur.close()

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.implicitly_wait(10)

conn = db_connect()

pages = get_links(static_pages)

fail_count = 0
success_count = 0
for page in pages:
    #time.sleep(5)
    driver.get(page)
    has_form = page_has_form(driver)

    if has_form:
        phone = get_phone()
        form_input_without_email = generate_form_input(phone)
        sent_forms_id, sent_received_id = insert_into_sent_forms_and_sent_received(conn, form_input_without_email)
        form_input = reset_email_in_form_input(form_input_without_email, sent_received_id)
        update_sent_forms_with_email(conn, sent_forms_id, form_input)
        if fillout_form(driver, form_input, fail_count):
            sent_flag = True
            success_count = success_count + 1
        else:
            sent_flag = False
            fail_count = fail_count + 1

        update_sent_forms_with_sent_flag(conn, sent_forms_id, sent_flag)

print('failure count: ', fail_count)
print('success count: ', success_count)
driver.quit()

print('Woohoo! No errors.')
