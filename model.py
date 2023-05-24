import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        
    def __repr__(self):
        return f"User: ID={self.user_id} Username={self.username}"
    
class Book(db.Model):
    __tablename__ = "books"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_title = db.Column(db.String, nullable=False)
    book_pic = db.Column(db.String, nullable=False)
    book_price = db.Column(db.String, nullable=False)
    book_page = db.Column(db.String, nullable=False)
    
    def __init__(self, book_title, book_pic, book_price, book_page):
        self.book_title = book_title
        self.book_pic = book_pic
        self.book_price = book_price
        self.book_page = book_page

    def __repr__(self):
        return f"<Book: ID={self.book_id} Title={self.book_title}"

      
def connect_to_db(app):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        print("Connected to the db!")


   
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    
