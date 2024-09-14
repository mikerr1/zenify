import time

from zenify.utils.selenium.contants import (
    FB_LOGIN_PAGE,
    FB_LOGIN_PAGE_ELEMENTS
)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def fb_login(driver, username, password):
    print("LOGGING IN TO FACEBOOK..")
    global FB_LOGIN_PAGE
    global FB_LOGIN_PAGE_ELEMENTS

    driver.get(FB_LOGIN_PAGE)
    time.sleep(5)
    assert driver.title == "Log in to Facebook"

    email = driver.find_element(
        FB_LOGIN_PAGE_ELEMENTS["login"]["email"]["by"],
        FB_LOGIN_PAGE_ELEMENTS["login"]["email"]["value"]
    )
    [email.send_keys(Keys.BACKSPACE) for _ in range(50)]
    email.send_keys(username)

    passw = driver.find_element(
        FB_LOGIN_PAGE_ELEMENTS["login"]["passw"]["by"],
        FB_LOGIN_PAGE_ELEMENTS["login"]["passw"]["value"]
    )
    [passw.send_keys(Keys.BACKSPACE) for _ in range(20)]
    passw.send_keys(password)

    submit = driver.find_element(
        FB_LOGIN_PAGE_ELEMENTS["login"]["submit"]["by"],
        FB_LOGIN_PAGE_ELEMENTS["login"]["submit"]["value"]
    )
    submit.click()
    time.sleep(10)