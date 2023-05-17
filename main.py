import time
from bs4 import BeautifulSoup #pip install bs4.
import requests #pip install requests. Acts as a person going and getting info from a site.

# print('Price Limit:')
# high_price = input('>') #searches for the specific input string. Not a greater than function.
# print(f'Filtering out higher prices')

def get_books():
    html_text = requests.get('https://books.toscrape.com/catalogue/category/books/classics_6/index.html').text #uses URL of website to be scraped.
    soup = BeautifulSoup(html_text, 'lxml') #pip install lxml.
    classics = soup.find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3') #finds all li tags with this
    for index, classic in enumerate(classics): #iterates over all objects found in classics variable.
        book_stock = classic.find('p', class_ = 'instock availability').text.replace(' ', '') #finds all books listed as Instock.
        if 'Instock' in book_stock: 
            book_title = classic.find('h3').text #gets title info and displays it as a string rather than html element
            book_price = classic.find('p', class_='price_color').text #gets price info and displays it as a string rather than html element
            book_page = classic.article.h3.a['href'] #gets value of href in the <a> tag.
            # if high_price not in book_price: #if specific value of variable is not present:
            with open(f'books/{index}.txt', 'w') as f:
                f.write(f'Book Title: {book_title} \n')
                f.write(f'Book Price: {book_price} \n')
                f.write(f'In Stock: {book_stock.strip()} \n')
                f.write(f'Book Page: {book_page}')
            print(f'Book Saved: {book_title}')





if __name__ == "__main__":
    while True: #this will run get_books function so long as name == "main".
        get_books()
        time_wait = 24 #hours variable
        time.sleep(time_wait * 3600) #this is a delay between runs of the program in seconds. 24 * 3600 seconds is 1 day.