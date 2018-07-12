from selenium import webdriver
import getpass
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

looping = True

def start():
    global driver
    driver = webdriver.Chrome("D:/Other software/chromedriver_win32/chromedriver.exe")
    driver.set_page_load_timeout(30)
    my_url = 'https://www.facebook.com/'
    driver.get(my_url)
    driver.maximize_window()
    email = input("Email: ")
    pw = getpass.getpass()
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("pass").send_keys(pw)
    driver.find_element_by_id("loginbutton").click()
    driver.get("https://www.facebook.com/messages/t/")
    get_top_convos()
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

#the problem is with the freaking notification pop up!
def download_pics(convo):
    global looping
    looping = True
    choose_convo(convo)
    while(looping):
        download_pic()
        press_next()

def download_latest(range):
    return None

def press_esc():
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("_4-od")).perform()
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_387s")))
        driver.find_element_by_class_name("_387s").click()
    except ElementNotVisibleException:
        print("Escape button is not visible")

def get_top_convos():
    global names
    names = driver.find_elements_by_class_name("_1ht6")
    print("\nShowing the top " + str(len(names)) + " conversations:\n")
    print_choices(names)
    print("\n")

def print_choices(arr):
    for x in range(0, len(arr)):
        print(str(x) + ": " + arr[x].text)

def choose_convo(i):
    global looping
    names[i].click()
    try:
        driver.implicitly_wait(1)
        driver.find_element_by_class_name("_3m31").click()
    except NoSuchElementException:
        looping = False
        print("No pictures in this conversation")

def download_pic():
    global looping
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("_4-od")).perform()
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Download")))
        driver.find_element_by_link_text("Download").click()
    except ElementNotVisibleException:
        looping = False
        print("Download button is not visible")
    except TimeoutException:
        looping = False
        print("Timed out, waited for a Download button for too long")

def press_next():
    global looping
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("_4-od")).perform()
    try:
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "_2bbc")))
        driver.find_element_by_class_name("_2bbc").click()
    except ElementNotVisibleException:
        looping = False
        print("Next button is not visible")
    except NoSuchElementException:
        looping = False
        print("Next button is not there, are you looking at the last picture?")
    except TimeoutException:
        looping = False
        print("Next button is not there, must have reached last picture")

def press_prev():
    global looping
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("_4-od")).perform()
    try:
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "_2bbb")))
        driver.find_element_by_class_name("_2bbb").click()
    except ElementNotVisibleException:
        looping = False
        print("Previous button is not visible, can't click it")
    except NoSuchElementException:
        looping = False
        print("Previous button is not there, are you looking at the first picture?")
    except TimeoutException:
        looping = False
        print("Prev button is not there, must have reached last picture")