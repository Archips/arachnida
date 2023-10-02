import hashlib
import io
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image
from selenium import webdriver

def get_content_from_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_content = driver.page_source
    driver.quit()
    return page_content

def parse_image_urls(content, classes, location, source):
    soup = BeautifulSoup(content, features="lxml")
    results = []
    results = soup.findAll('img')
    print(results)
    # for a in soup.findAll(attrs={'class': classes}):
    #     name = a.find(location)
    #     if name not in results:
    #         results.append(name.get(source))
    return results

def save_urls_to_csv(image_urls):
    df = pd.DataFrame({'links': image_urls})
    df.to_csv("links.csv", index=False, encoding="utf-8")

def get_and_save_image_to_file(image_url, output_dir):
    response = requests.get(image_url, headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})
    image_content = response.content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert("RGB")
    filename = hashlib.sha1(image_content).hexdigest()[:10] + ".png"
    file_path = output_dir / filename
    image.save(file_path, "PNG", quality=80)

def main():
   url = "http://books.toscrape.com/"
   content = get_content_from_url(url)
   image_urls = parse_image_urls(
       content=content, classes="s-item__image-wrapper image-treatment", location="img", source="src",
   )
   save_urls_to_csv(image_urls)

   for image_url in image_urls:
       get_and_save_image_to_file(
           image_url, output_dir=Path("../img"),
       )


if __name__ == "__main__":  # Only executes if imported as a main file.
   main()
