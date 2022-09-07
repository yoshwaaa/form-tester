#!/usr/bin/env 
        pass

    try:
        phone = driver.find_element_by_name("phone_number")
        phone.send_keys("4073250884")
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
        address.send_keys("This is your hourly form test!")
    except(NoSuchElementException, AttributeError):
        pass

    try:
        city = driver.find_element_by_name("user_city")
        city.send_keys("Automation")
    except(NoSuchElementException):
        pass

    try:
        state = driver.find_element_by_name("user_state")
        state.send_keys('KS')
        state.send_keys(Keys.RETURN)
    except(NoSuchElementException):
        pass

    try:
        user_zip = driver.find_element_by_name("user_zip")
        user_zip.send_keys("66213")
    except(NoSuchElementException):
        pass

    try:
        message = driver.find_element_by_name("body_message")
        message.send_keys("This form test should only go to Josh.  If lost,\
                          please return to joshua.lohse@mesotheliomaguide.com")
    except(NoSuchElementException):
        pass

    # submit on the name input
    try:
        name = driver.find_element_by_name("full_name")
        name.send_keys(Keys.RETURN)
    except(NoSuchElementException):
        pass

    try:
        driver.find_element_by_class_name('success')
        return True
    except(NoSuchElementException):
        return False

# change path to location of the file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# start display and driver
display = Display(visible=0, size=(1120, 550))
display.start()
driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.implicitly_wait(30)

# connect to db
conn = db_connect()

"""
http://stackoverflow.com/a/4992124
try: / except Exception as e: around the error-prone part of the code to ensure
that the driver, database, and Xvfb always close.
"""
try:
    page = static_pages[randint(0, len(static_pages)-1)]
    driver.get(page)
    url = driver.current_url
    title = driver.title[:100]
    sent_flag = False

    # log new page and log new test
    cur = conn.cursor()
    cur.execute("SELECT * FROM page WHERE url = %s", [url])
    db_page = cur.rowcount
    cur.close()

    if not bool(db_page):
        cur = conn.cursor()
        cur.execute("INSERT INTO page (title, url, active)\
                    VALUES (%s, %s, %s)", [title, url, True])
        conn.commit()
        cur.close()

    cur = conn.cursor()
    cur.execute("SELECT id FROM page WHERE url = %s", [url])
    page_id = cur.fetchall()[0][0]

    cur = conn.cursor()
    cur.execute("INSERT into test_log (page_id, test_result) VALUES (%s, %s)\
                RETURNING id", [page_id, sent_flag])
    id_of_test_log = cur.fetchone()[0]
    conn.commit()
    cur.close()

    if fillout_form(driver):
        sent_flag = True
        cur = conn.cursor()
        cur.execute("UPDATE test_log SET test_result = %s WHERE id = %s",
                    [sent_flag, id_of_test_log])
        conn.commit()
        cur.close()

except Exception as e:
    print(e)

# close display, driver and database
display.stop()
driver.quit()
conn.close()

if not sent_flag:
    log = "There may be a problem with the form on page {}".format(page)

    fromaddr = 'joshatbcbh@gmail.com'
    toaddr = 'joshua.lohse@mesotheliomaguide.com'
    msg = MIMEMultipart()

    msg['From'] = 'joshatbcbh@gmail.com'
    msg['To'] = 'joshua.lohse@mesotheliomaguide.com'
    msg['Subject'] = 'SERVER ALERT -- FORMS'

    body = log

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, 'topher123')
    recipients = ['joshua.lohse@mesotheliomaguide.com',
                  'acbilimoria.bcbh@gmail.com']
    for toaddr in recipients:
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)

    server.quit()
