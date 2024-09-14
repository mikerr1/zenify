import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import bs4


def _in_viewport(driver: webdriver, element):
    script = (
        "for(var e=arguments[0],f=e.offsetTop,t=e.offsetLeft,o=e.offsetWidth,n=e.offsetHeight;\n"
        "e.offsetParent;)f+=(e=e.offsetParent).offsetTop,t+=e.offsetLeft;\n"
        "return f<window.pageYOffset+window.innerHeight&&t<window.pageXOffset+window.innerWidth&&f+n>\n"
        "window.pageYOffset&&t+o>window.pageXOffset"
    )
    return driver.execute_script(script, element)


def scroll_to_element(driver,
                      element,
                      sleep=0.5):
    while not _in_viewport(driver, element):
        # print(_in_viewport(driver, element), sep=" ")
        ActionChains(driver) \
            .send_keys(Keys.PAGE_DOWN) \
            .perform()
        time.sleep(sleep)


def wait_for_element(driver,
                     element_name,
                     element_dict,
                     timeout=5):
    # print(element_dict)
    element_visible = False
    retries = timeout
    el = None
    while not element_visible:
        try:
            for k, v in element_dict.items():
                if k == "class_name":
                    el = driver.find_element(By.CLASS_NAME, v)
                elif k == "css_selector":
                    el = driver.find_element(By.CSS_SELECTOR, v)
                elif k == "xpath":
                    el - driver.find_element(By.XPATH, v)

            if el.is_displayed():
                # print(f"Element is found..")
                element_visible = True
        except Exception as e:
            print(f"Waiting for element.. {element_name} still not visible..")

            retries -= 1 if retries > 0 else ...
            if retries == 0:
                return None
            time.sleep(2)
    else:
        return el


def move_down(current_tag: bs4.element.Tag, number_of_moves: int):
    """
    Traverse the HTML recursively. Currently only support down move.
    :param current_tag:
    :param number_of_moves:
    :return:
    """
    # print("\n")
    # print("Current tag:", current_tag.name, "remaining moves", number_of_moves)
    # print("Current tag data:", str(current_tag)[:200])

    next_tag = None

    if number_of_moves < 1:
        # print("returning")
        return current_tag

    for children in current_tag.children:
        next_tag = children
        break

    if next_tag is not None:
        # print("Current tag", str(next_tag)[:200], "Move down 1")
        return move_down(next_tag, number_of_moves - 1)
    else:
        raise ValueError("Tag is none")


def goto_sibling(current_tag: bs4.element.Tag,
                 which_sibling) -> bs4.element.Tag:
    """
    Find sibling of the current tag. Which sibling should be key of a list
    0: to find next sibling
    1: to find second sibling and etc
    -1: to find the last sibling
    :param current_tag:
    :param which_sibling:
    :return:
    """
    siblings = current_tag.findNextSiblings()
    sibling = siblings[which_sibling]
    return sibling


def traverse_dom(soup: BeautifulSoup, func_map, debug=False):
    print("SCANNING HTML... ....")
    for item in func_map:
        if callable(item[0]):
            if debug: print(f"{item[0]} => {str(item[1])}")
            soup = item[0](soup, item[1])

    return soup

# Function to scroll down
# credit: https://scrapfly.io/blog/how-to-scroll-to-the-bottom-with-selenium/#:~:text=To%20scroll%20down%20a%20web,driver%20to%20the%20specified%20coordinates.
def scroll_down(driver):
    print("SCROLLING DOWN TO LOAD LISTING ITEMS..")
    prev_height = -1
    max_scrolls = 100
    scroll_count = 0

    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # give some time for new results to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height:
            break
        prev_height = new_height
        scroll_count += 1
