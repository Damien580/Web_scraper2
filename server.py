from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms import NewUserForm, LoginForm
from model import Book, User, connect_to_db, db

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
           

   
# db.create_all()


if __name__ == "__main__":
    from model import Book, User, connect_to_db, db
    connect_to_db(app)
    with app.app_context():
        db.create_all()
    app.run(debug = True, port = 8001, host = "localhost")
    