import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def get_url(search_term):
    template = "https://www.amazon.com/s?k={}"
    search_term = search_term.replace(" ", "+")

    url = template.format(search_term)
    url += "&page={}"

    return url

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get("href")
    try:
        price_parent = item.find("span", "a-price")
        price = item.find("span", "a-offscreen").text
    except AttributeError:
        return
    try:
        rating = item.i.text
        number_of_ratings = item.find("span", "a-size-base s-underline-text").text
    except AttributeError:
        rating = ""
        number_of_ratings = ""

    result = (description,price,rating,number_of_ratings,url)
    return result

def main():
    driver = webdriver.Chrome()
    url = "https://www.amazon.com"
    driver.get(url)

    records = []

    url = get_url(input("What would like me to scrape on amazon.com? "))

    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        for items in results:
            record = extract_record(items)
            if record:
                records.append(record)
    driver.close()

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "Price", "Rating", "Review Count", "Url"])
        writer.writerows(records)
 
    read_file = pd.read_csv (r'C:\Users\clift\OneDrive\Documents\GitHub\Amazon-Webscrape\results.csv')
    read_file.to_excel (r'C:\Users\clift\OneDrive\Documents\GitHub\Amazon-Webscrape\results.xlsx', index = None, header=True)

main()