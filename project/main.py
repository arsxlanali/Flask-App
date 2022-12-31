from flask import Blueprint, render_template
from flask_login import login_required, current_user
import sqlite3
from .models import shop
from . import db
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')




@main.route('/home')
def home():
    return render_template('home.html', name=current_user.name)

@main.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', name=current_user.name)



breed = ['Red', 'Blue', 'Black', 'Breed']
size = ['Red', 'Blue', 'Black', 'Size']
@main.route('/shop')
def shop():
    con = sqlite3.connect('instance\db.sqlite')
    cur = con.cursor()    
    cur.execute("SELECT * FROM shop;")
    items = cur.fetchall()
    return render_template('shop.html', items=items, len=len(items), breed=breed, size=size)

@main.route('/shop/<id>')
def shopDetials(id):
    id = 3
    con = sqlite3.connect('instance\db.sqlite')
    cur = con.cursor()    
    cur.execute("SELECT * FROM shop where id = ?", (id,))
    row = cur.fetchone()
    postUrl = row[1]
    title = row[2]
    details = row[3]
    review = row[4]
    imgUrl = row[5]
    return render_template('shopdetails.html', postUrl=postUrl,title=title,
                           details=details, review=review,imgUrl=imgUrl)
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
