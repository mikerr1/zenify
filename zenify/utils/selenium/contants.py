from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from zenify.utils.selenium.common import *

FB_LOGIN_PAGE = "https://www.facebook.com/login.php/"

FB_LOGIN_PAGE_ELEMENTS = {
    "login": {
        "email": {"by": By.ID, "value": "email"},
        "passw": {"by": By.ID, "value": "pass"},
        "submit": {"by": By.ID, "value": "loginbutton"}
    }
}

FB_MAP_MARKETPLACE_RENTALS = (
    # Facebook marketplace rental listings
    (move_down, 3),  # move down 3
    (goto_sibling, -1),  # go to last sibling
    (move_down, 1),  # move down 1
    (goto_sibling, 0),  # go to next sibling
    (move_down, 2),  # move down 2
    (goto_sibling, 0)  # go to next sibling
)

