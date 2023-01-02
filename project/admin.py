from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_login import login_required, current_user
import sqlite3
from .models import User
from . import db
main = Blueprint('main', __name__)


@main.route('/admin')
@login_required
def admin():
    return render_template('admin.html', name=current_user.name)
