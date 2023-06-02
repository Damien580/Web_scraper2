import time
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms import LikeForm, NewUserForm, LoginForm
from model import Book, Like, User, connect_to_db, db
import scraper


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
    if current_user.is_authenticated:
        logout_user()
        flash("You are Logged Out!")
    else:
        flash("You are not Logged In!")
    return redirect("/")

@app.route("/books")
@login_required
def all_books():
    like_form = LikeForm()
    all_books = scraper.get_all_books()
    return render_template("books.html", books=all_books, like_form=like_form)

@app.route("/books", methods=["POST"])
@login_required
def like():
    like_form = LikeForm()
    
    if like_form.validate_on_submit():
        likes = like_form.like.data
        new_like=Like(likes)
        db.session.add(new_like)
        db.session.commit()
        flash(f"{Book.book_title} Liked!")
    else:
        flash("Please try again!")
    return render_template("books.html", books=all_books, like_form=like_form)


if __name__ == "__main__":
    connect_to_db(app)
    with app.app_context():
        db.create_all()
        scraper.get_books()
    app.run(debug = True, port = 8001, host = "localhost")
    