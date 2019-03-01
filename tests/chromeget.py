# coding=utf8
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# 以无头方式使用 Chrome 而无需再采用PhantomJS的方式
chrome_options = Options()
chrome_options.add_argument("--headless") # 指定采用无头方式

browser = webdriver.Chrome(executable_path="/usr/local/Caskroom/chromedriver/2.46/chromedriver", chrome_options=chrome_options)

browser.get("http://www.baidu.com")
#browser.get("https://s.taobao.com/search?q=Vue2&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306")
browser.implicitly_wait(1)

element = browser.find_element_by_id('kw')
#button = browser.find_element_by_css_selector('form button.btn-search')

print(element.get_attribute('name'))
browser.close()