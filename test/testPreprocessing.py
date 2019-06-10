from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from pytesseract import *
import time
import datetime

profile = webdriver.FirefoxProfile()
browser=webdriver.Firefox()
browser.get('https://www.zhihu.com/signup?next=%2F')
browser.implicitly_wait(3)
browser.find_element_by_xpath("//div[contains(@class,SignFlowHomepage)]")