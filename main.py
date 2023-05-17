from bs4 import BeautifulSoup #pip install bs4.
import requests #pip install requests. Acts as a person going and getting info from a site.

html_text = requests.get('https://books.toscrape.com/catalogue/category/books/classics_6/index.html').text #uses URL of website to be scraped.
soup = BeautifulSoup(html_text, 'lxml') #pip install lxml.
classics = soup.find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
for classic in classics:
    book_title = classic.find('h3').text
    book_price = classic.find('p', class_='price_color').text
    # book_stock = classic.find('p', class_ = 'instock availability').text.replace(' ', '')


print(f"""
      Book Title: {book_title}
      Book Price: {book_price}
      """)