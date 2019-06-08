
from selenium import webdriver

driver = webdriver.Chrome() 
driver.get(request_url)

srcs = html.xpath(src_xpath) 
titles = html.xpath(title_path)

for src, title in zip(srcs, titles):

	download(src, title.text)