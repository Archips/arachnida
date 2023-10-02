import requests


url = 'https://oxylabs.io/blog'
response = requests.get(url)


print(response)

from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title)

blog_titles = soup.find_all('a', class_='e1dscegp1')
for title in blog_titles:
    print(title.text)
# Output:
# Prints all blog tiles on the page
