import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "http://books.toscrape.com/"

def fetch_site(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
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

def save_to_csv(all_books, file_name):
    df = pd.DataFrame(all_books)
    df.to_csv(file_name)

response = fetch_site(url)
all_books = extract_book_details(response)
save_to_csv(all_books, "book.csv")
print(all_books)