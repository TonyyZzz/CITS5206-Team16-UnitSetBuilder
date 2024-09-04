from flask import render_template, request, jsonify
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from app.models import User
from app import login_manager, bcrypt
from . import auth

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
    
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None