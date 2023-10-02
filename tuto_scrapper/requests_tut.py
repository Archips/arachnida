import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Firefox()

driver.get('https://blog.holbertonschool.com/hack-virtual-memory-stack-registers-assembly-code/')

results = []

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

for element in soup.findAll(attrs={'class': 'page-main-title'}):
    name = element.find('a')
    if name not in results:
        results.append(name.text)

df = pd.DataFrame({'Name': results})
df.to_csv('names.csv', index=False, encoding='utf-8')
