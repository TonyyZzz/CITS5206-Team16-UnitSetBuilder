from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from app.models import User
from app import login_manager, bcrypt, db
from . import auth

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({'status': 'success', 'email': user.email})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid Username or Password'})
    else:
        return render_template('login.html')
    
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle register form submission
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({'status': 'error', 'message': 'Username already exists'})
        else:
            new_user = User(username=username, email=email, password_hash=bcrypt.generate_password_hash(password).decode('utf-8'))
            # Add new user to the database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'status': 'success'})
    else:
        return render_template('register.html')