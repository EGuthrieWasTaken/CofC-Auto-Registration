#!/usr/bin/python3
# autoRegister.py
# Ethan Guthrie
# 11/06/2019
# Registers for classes at a set time.

# Datetime library allows for comparison of times to ensure program runs at the correct time.
from datetime import datetime, time
# Getpass allows for a password to be typed into the terminal session wiht echo off.
from getpass import getpass
# Selenium's webdriver library allows for webpage control from Python. You will need to run "[sudo] pip install selenium" to import
#      this library. The documentation for this python module can be read with the link below.
#      https://seleniumhq.github.io/selenium/docs/api/py/index.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
# System library allows for command line arguments.
import sys
# Time library allows program to sleep between time checks (so that program isn't too demanding).
from time import sleep

def main():
    # Initializing variables.
    register_time_str = ""
    filename = ""
    headless = False
    password = ""
    skip = False
    term = ""
    username = ""

    # Checking commmand line arguments.
    for i in range(0, len(sys.argv)):
        if sys.argv[i] == "autoRegister.py":
            args = sys.argv[i + 1:]
    try:
        for i in range(0, len(args)):
            if not skip and args[i][0] != '-':
                filename = args[i]
            if not skip and args[i][0] == '-':
                if args[i][1] == "h":
                    print("Usage:\tpython3 autoRegister.py [-defmpstuh] [file]")
                    print("Options:\t-d\tProvide a date (YYYY-MM-DD)")
                    print("\t\t-e\tSilence GUI output (run Selenium headless)")
                    print("\t\t-f\tSet registration term to Fall")
                    print("\t\t-m\tSet registration term to Summer")
                    print("\t\t-p\tProvide MyCharleston password")
                    print("\t\t-s\tSet registration term to Spring")
                    print("\t\t-t\tProvide a text file of CRNs")
                    print("\t\t-u\tProvide MyCharleston username")
                    print("\n\t\t-h\tDisplay this help message")
                    return
                elif args[i][1] == "d" and not register_time_str:
                    register_time_str = args[i + 1]
                    skip = True
                elif args[i][1] == "e" and not headless:
                    headless = True
                elif args[i][1] == "f" and not term:
                    term = "fall"
                elif args[i][1] == "m" and not term:
                    term = "summer"
                elif args[i][1] == "p" and not password:
                    password = args[i + 1]
                    skip = True
                elif args[i][1] == "s" and not term:
                    term = "spring"
                elif args[i][1] == "t" and not filename:
                    filename = args[i + 1]
                    skip = True
                elif args[i][1] == "u" and not username:
                    username = args[i + 1]
                    skip = True
                else:
                    print("Usage:\tpython3 autoRegister.py [-defmpstuh] <file>")
                    print("\tUse \"python3 autoRegister.py -h\" for help with options")
                    return
            else:
                skip = False
    except:
        print("Usage:\tpython3 autoRegister.py [-defmpstuh] <file>")
        print("\tUse \"python3 autoRegister -h\" for help with options")
        return
    if not register_time_str:
        register_time_str = str(input("Enter date of registration (YYYY-MM-DD):\t"))
    login_time_str = register_time_str + " 07:59"
    register_time_str += " 08:00"
    if filename:
        course_codes = get_items_from_txt(filename)
    else:
        course_codes = []
        code_count = int(eval(input("Enter number of course codes:\t")))
        for i in range(0, code_count):
            course_codes.append(int(eval(input("Enter CRN #" + str(i + 1) + ":\t"))))
    if not username:
        username = input("Enter MyCharleston username:\t")
    if not password:
        while True:
            password = getpass("MyCharleston Password:\t")
            password2 = getpass("Confirm MyCharleston Password:\t")
            if password == password2:
                break
            else:
                print("Passwords do not match!\n")
    if not term:
        now = datetime.now()
        if now.month > 8:
            term = "spring"
        elif now.month == 3:
            term = "summer"
        else:
            term = "fall"

    # Converting login and registration times to datetime format.
    login_time = datetime.strptime(login_time_str, "%Y-%m-%d %H:%M")
    register_time = datetime.strptime(register_time_str, "%Y-%m-%d %H:%M")
    
    # Waiting until login time.
    curr_time = datetime.now()
    if login_time > curr_time:
        day = register_time.strftime("%-d")
        if day[-1] == "1" and day != "11":
            date_suffix = "st"
        elif day[-1] == "2" and day != "12":
            date_suffix = "nd"
        elif day[-1] == "3" and day != "13":
            date_suffix = "rd"
        else:
            date_suffix = "th"
        print(register_time.strftime("This program will wait until %-I:%M%p on %A, %B %-d" + date_suffix + ", %Y to register for the " + term.capitalize() + " term.\nPlease note: This program will login to MyCharleston one minute prior to registration. This is normal."))
    while login_time > curr_time:
        sleep(10)
        curr_time = datetime.now()

    # Initializing WebDriver
    options  = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(10)

    # Logging in to MyCharleston.
    print("Logging in to MyCharleston....")
    if not myCharleston_login(driver, username, password):
        print("Failed to login to MyCharleston!")
        return

    # Waiting until registration time.
    curr_time = datetime.now()
    while register_time > curr_time:
        sleep(2)
        curr_time = datetime.now()

    # Registering for courses
    print("Registering for courses....")
    if not register(driver, term, course_codes):
        print("Failed to register!")
        return
    print("Registration complete!")

def get_items_from_txt(filename):
    with open(filename, 'r') as file:
        items = [item.rstrip('\n') for item in file]
    return items

def myCharleston_login(driver, username, password):
    try:
        driver.get("https://my.cofc.edu/cp/home/displaylogin")
        driver.find_element_by_name("user").send_keys(username)
        driver.find_element_by_name("pass").send_keys(password)
        driver.find_element_by_id("login_btn").click()
        return True
    except Exception as e:
        print(e)
        return False

def register(driver, registration_term, course_codes):
    try:
        now = datetime.now()
        if registration_term == "fall":
            menu_value = str(now.year + 1) + "10"
        elif registration_term == "spring":
            menu_value = str(now.year + 1) + "20"
        else:
            menu_value = str(now.year) + "30"
        driver.get("https://my.cofc.edu/render.UserLayoutRootNode.uP?uP_tparam=utf&utf=%2fcp%2fip%2flogin%3fsys%3dsctssb%26url%3dhttps://ssb.cofc.edu:9710/prod/bwskfreg.P_AltPin")
        driver.switch_to.frame(driver.find_element_by_name("content"))
        sleep(1)
        term_selector = Select(driver.find_element_by_id("term_id"))
        term_selector.select_by_value(menu_value)
        driver.find_element_by_xpath("/html/body/div[3]/form/input").click()
        sleep(3)

        counter = 0
        for code in course_codes:
            counter += 1
            driver.find_element_by_id("crn_id" + str(counter)).send_keys(code)
        driver.find_element_by_xpath("/html/body/div[3]/form/input[19]").click()
        sleep(10)
        return True
    except Exception as e:
        print(e)
        return False

main()