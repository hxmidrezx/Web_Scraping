import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin

url = "http://books.toscrape.com/catalogue/page-{}.html"

def fetch_site(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None

def extract_book_details(content):
    soup = BeautifulSoup(content, "html.parser")
    all_books = []
    books = soup.find_all("article", class_="product_pod")
    for book in books:
        title = book.h3.a.attrs["title"]
        price = book.find("p", class_ = "price_color").text
        availability = book.find("p", class_ = "availability").text.strip()
        rating = book.find("p", class_ = "star-rating")["class"][1]
        dict_book = {
            "title" : title,
            "price" : price,
            "availability" : availability,
            "rating" : rating
        }
        all_books.append(dict_book)
    return all_books

def extract_img(content, url, i):
    soup = BeautifulSoup(content, "html.parser")
    images = soup.find_all("img")
    os.makedirs(f"all_images/page_{i}_images", exist_ok = True)
    for img in images:
        src = img["src"]
        img_url = urljoin(url, src)
        img_name = os.path.basename(src)
        img_data = fetch_site(img_url)
        with open(os.path.join(f"all_images/page_{i}_images", img_name),"wb")as f :
            f.write(img_data)
def save_to_csv(all_books, file_name):
    df = pd.DataFrame(all_books)
    df.to_csv(file_name)

books = []
os.makedirs("all_images", exist_ok = True)
i = 1
while True :
    response = fetch_site(url.format(i))
    print(url.format(i))
    if response :
        extract_img(response, url, i)
        all_books = extract_book_details(response)
        books = books + all_books
        i += 1
    else :
        break
save_to_csv(books, "book.csv")