import time
from bs4 import BeautifulSoup
import requests

def get_books():
    index = 0
    for page_number in range(1, 51):
        url = 'https://books.toscrape.com/catalogue/category/books_1/page-{}.html'.format(page_number)
        html_text = requests.get(url).text #uses URL of website to be scraped.
        soup = BeautifulSoup(html_text, 'lxml')
        books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
        for book in books:
            book_stock = book.find('p', class_='instock availability').text.replace(' ', '')
            if 'Instock' in book_stock:
                book_title = book.find('h3').text
                book_price = book.find('p', class_='price_color').text
                book_page = book.article.h3.a['href']
                with open(f'books/{index}.txt', 'w') as f:
                    f.write(f'Book Title: {book_title}\n')
                    f.write(f'Book Price: {book_price}\n')
                    f.write(f'In Stock: {book_stock.strip()}\n')
                    f.write(f'Book Page: {book_page}')
                print(f'Book Saved: {book_title}')
                index += 1





if __name__ == "__main__":
    while True: #this will run get_books function so long as name == "main".
        get_books()
        time_wait = 24 #hours variable
        time.sleep(time_wait * 3600) #this is a delay between runs of the program in seconds. 24 * 3600 seconds is 1 day.