import time
from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms import NewUserForm, LoginForm
from model import Book, User, connect_to_db, db
from main import get_books
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = "Books"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def home():
    login_form = LoginForm()
    return render_template("home.html", login_form=login_form)
    
@app.route("/new_user", methods=['GET', 'POST'])
def new_user():
    new_user_form = NewUserForm()
    
    if new_user_form.validate_on_submit():
        new_username = new_user_form.new_username.data
        new_password = new_user_form.new_password.data
        new_email = new_user_form.new_email.data
        new_user=User(new_username, new_password, new_email)
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
            flash(f'Welcome {new_username}, Please Log In!!!')
        return redirect(url_for("home"))
    else:
        flash('Please Try Again') 
    return render_template("new_user.html", new_user_form=new_user_form)
           
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    
    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                login_user(user)
                flash("Logged In!")
        else:    
            flash("Either the password or username is incorrect!")

    return render_template("home.html", login_form=login_form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You are Logged Out!")
    return redirect("/")

@app.route("/books")
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
                book_pic = book.article.div.a['href'].text
                book_price = book.find('p', class_='price_color').text #gets price info and displays it as a string rather than html element.
                book_page = book.article.h3.a['href'].text #gets value of href in the <a> tag inside the <h3> inside the <article> tag.
                book = Book(book_title, book_pic, book_price, book_page)
                db.session.add(book)
                db.session.commit()
                
                index += 1 #adds 1 to index to move the iteration to the next book.
    return render_template("books.html", books=books)



if __name__ == "__main__":
    from model import Book, User, connect_to_db, db
    connect_to_db(app)
    with app.app_context():
        db.create_all()
    app.run(debug = True, port = 8001, host = "localhost")
    while True: #this will run get_books function so long as name == "main".
        with app.app_context():
            get_books()
        time_wait = 24 #hours variable
        time.sleep(time_wait * 3600) #this is a delay between runs of the program in seconds. 24 * 3600 seconds is 1 day.
    