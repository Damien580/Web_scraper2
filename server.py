from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms import NewUserForm
from model import Book, User, connect_to_db, db

app = Flask(__name__)
app.secret_key = "Books"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)