import re
import time
from bs4 import BeautifulSoup
import requests
from model import Book, db


def get_books():
    index = 0
    for page_number in range(1, 51):
        url = 'https://books.toscrape.com/catalogue/category/books_1/page-{}.html'.format(page_number)
        html_text = requests.get(url).text #uses URL of website to be scraped.
        soup = BeautifulSoup(html_text, 'lxml') #pip install lxml.
        books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3') #finds all li tags with this class.
        for book in books:
            book_stock = book.find('p', class_='instock availability').text.replace(' ', '') #finds all books listed as Instock.
            if 'Instock' in book_stock:
                book_title = book.find('h3').text #gets title info and displays it as a string rather than html element.
                book_pic = book.find('a', attrs={'href': re.compile("^https://")})
                book_price = book.find('p', class_='price_color').text #gets price info and displays it as a string rather than html element.
                book_page = book.article.h3.a['href'] #gets value of href in the <a> tag inside the <h3> inside the <article> tag.
                book = Book(book_title, book_pic, book_price, book_page)
                db.session.add(book)
                db.session.commit()
                
                index += 1 #adds 1 to index to move the iteration to the next book.

def get_all_books():
    return Book.query.all()



if __name__ == "__main__":
    while True: #this will run get_books function so long as name == "main".
        get_books()
        time_wait = 24 #hours variable
        time.sleep(time_wait * 3600) #this is a delay between runs of the program in seconds. 24 * 3600 seconds is 1 day.