from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_login import login_required, current_user
import sqlite3
from .models import User
from . import db
main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home.html', name=current_user.name)
    else:
        return render_template('home.html', name='')





@main.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', name=current_user.name)
    else:
        return render_template('home.html', name="")

@main.route('/aboutus')
def aboutus():
    if current_user.is_authenticated:
        return render_template('aboutus.html', name=current_user.name)
    else:
        return render_template('aboutus.html', name="")




breed = ['Red', 'Blue', 'Black', 'Breed']
size = ['Red', 'Blue', 'Black', 'Size']
@main.route('/shop')
def shop():
    con = sqlite3.connect('instance\db.sqlite')
    cur = con.cursor()    
    cur.execute("SELECT * FROM shop;")
    items = cur.fetchall()
    if current_user.is_authenticated:
        return render_template('shop.html', items=items, len=len(items), breed=breed, size=size, name=current_user.name)
    else:
        return render_template('shop.html', items=items, len=len(items), breed=breed, size=size, name="")


@main.route('/shop/<id>')
@login_required
def shopDetials(id):
    con = sqlite3.connect('instance\db.sqlite')
    cur = con.cursor()    
    cur.execute("SELECT * FROM shop where id = ?", (id,))
    row = cur.fetchone()
    postUrl = row[1]
    title = row[2]
    details = row[3]
    review = row[4]
    imgUrl = row[5]
    price = row[6]
    return render_template('shopdetails.html', postUrl=postUrl,title=title,
                           details=details, review=review, imgUrl=imgUrl, price=price, id=id, name=current_user.name)

@main.route('/shop/checkout/<id>')
@login_required
def checkout(id):
    con = sqlite3.connect('instance\db.sqlite')
    cur = con.cursor()    
    cur.execute("SELECT * FROM shop where id = ?", (id,))
    row = cur.fetchone()
    postUrl = row[1]
    details = row[3]
    price = row[6]
    return render_template('checkout.html', postUrl=postUrl,
                           details=details, price=price, id=id, name=current_user.name)

@main.route('/grooming')
def grooming():
    if current_user.is_authenticated:
        return render_template('grooming.html', name=current_user.name)
    else:
        return render_template('grooming.html', name="")


@main.route('/contact')
def contact():
    if current_user.is_authenticated:
        return render_template('contact.html', name=current_user.name)    
    else:
        return render_template('contact.html', name="")


@main.route("/shop/checkout/farward/<id>", methods=['POST'])
@login_required
def farward(id):
    con = sqlite3.connect('instance\db.sqlite')
    cur = con.cursor()
    cur.execute("SELECT * FROM shop where id = ?", (id,))
    row = cur.fetchone()
    postUrl = row[1]
    title = row[2]
    details = row[3]
    price = row[6]
    if request.form.getlist('PayPal'):
        return redirect("https://www.paypal.com/pk/home", code=302)
    elif request.form.getlist('Credit'):
        # print("dffdfdfd")
        return render_template('creditcard.html', title=title, name=current_user.name)
    else:
        return redirect(url_for('main.checkout',  postUrl=postUrl,
                                details=details, price=price, id=id, name=current_user.name))


@main.route('/finish')
@login_required
def finish():
    if current_user.is_authenticated:
        return render_template('finish.html', name=current_user.name)
    else:
        return render_template('finish.html', name="")


@main.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated:
        name = current_user.name
        con = sqlite3.connect('instance\db.sqlite')
        cur = con.cursor()
        cur.execute("SELECT * FROM user where name = ?", (name,))
        row = cur.fetchone()
        name = row[1]
        email = row[2]
        address = row[4]
        return render_template('profile.html', name=current_user.name, email=email, address=address)
    else:
        return render_template('profile.html', name="")


@main.route('/profile', methods=['POST'])
def update_profile():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    address = request.form.get('address')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, address=address,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@main.route('/admin')
@login_required
def admin():
    return render_template('admin.html', name=current_user.name)


@main.route('/adminshop')
@login_required
def adminshop():
    return render_template('adminshop.html', name=current_user.name)
