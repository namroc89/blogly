"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "hellomybaby12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    """redirects to users list"""
    return redirect("/users")


@app.route('/users')
def user_list():
    """Shows list of created users"""
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', users=users)


@app.route('/users/new')
def new_user_form():
    """Shows form to add a new user"""
    return render_template("new_user.html")


@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Uses form data to create new user and add to database. Redirects to home"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image = request.form["image"]
    image = image if image else None

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Shows user details"""
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route('/users/<user_id>/edit')
def get_edit_form(user_id):
    """brings up form to edit selected user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route('/users/<user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edits specified user and updates database"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    image = request.form["image"]
    user.image_url = image if image else None

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route('/users/<user_id>/delete')
def delete_confirmation(user_id):
    """Sends to page to confirm deletion"""
    user = User.query.get_or_404(user_id)
    return render_template("delete_user.html", user=user)


@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()

    db.session.commit()
    return redirect('/users')
