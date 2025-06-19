# Additional authentication utilities and routes
from flask import current_app
import logging
from models import db, User

def init_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        import firebase_admin
        from firebase_admin import credentials
        
        if not firebase_admin._apps:
            # In production, you would use a service account key file
            # cred = credentials.Certificate('path/to/serviceAccountKey.json')
            # firebase_admin.initialize_app(cred)
            
            # For development, initialize without credentials
            firebase_admin.initialize_app()
            logging.info("Firebase Admin SDK initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize Firebase: {e}")
        return False
    return True

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
# from models import db, User
from functools import wraps
from flask import jsonify, request
from flask_login import login_user, logout_user, current_user, login_required


# Blueprint setup
auth_bp = Blueprint('auth', __name__)

# Ensure login_required is defined before use



@auth_bp.route("/login")
def auth_login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template("login.html")

@auth_bp.route("/register")
def auth_register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template("register.html")

@auth_bp.route("/login", methods=["POST"])
def handle_login():
    if request.is_json:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        errors = {}
        if not email:
            errors['email'] = 'Email is required.'
        if not password:
            errors['password'] = 'Password is required.'
        if errors:
            return jsonify({'error': 'Validation error', 'errors': errors}), 400
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            session['user_id'] = user.id
            session['user_email'] = user.email
            return jsonify({'message': 'Login successful!', 'user': {'id': user.id, 'email': user.email, 'username': user.username}})
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    if not email or not password:
        flash('Email and password are required', 'error')
        return redirect(url_for('auth.auth_login'))
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=True)
        session['user_id'] = user.id
        session['user_email'] = user.email
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('auth.auth_login'))

@auth_bp.route("/register", methods=["POST"])
def handle_register():
    if request.is_json:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        confirm_password = data.get('confirm_password', '').strip()
        username = data.get('username', '').strip()
        errors = {}
        if not email:
            errors['email'] = 'Email is required.'
        if not password:
            errors['password'] = 'Password is required.'
        if not confirm_password:
            errors['confirmPassword'] = 'Confirm password is required.'
        if password != confirm_password:
            errors['confirmPassword'] = 'Passwords do not match.'
        if not username:
            errors['username'] = 'Username is required.'
        if len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters long.'
        if User.query.filter_by(email=email).first():
            errors['email'] = 'Email already registered.'
        if User.query.filter_by(username=username).first():
            errors['username'] = 'Username already taken.'
        if errors:
            return jsonify({'error': 'Validation error', 'errors': errors}), 400
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session['user_id'] = user.id
            session['user_email'] = user.email
            return jsonify({'message': 'Registration successful!', 'user': {'id': user.id, 'email': user.email, 'username': user.username}})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Registration failed. Please try again.'}), 500
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    username = request.form.get('username', '').strip()
    if not email or not password or not username:
        flash('All fields are required', 'error')
        return redirect(url_for('auth.auth_register'))
    if len(password) < 6:
        flash('Password must be at least 6 characters long', 'error')
        return redirect(url_for('auth.auth_register'))
    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'error')
        return redirect(url_for('auth.auth_register'))
    if User.query.filter_by(username=username).first():
        flash('Username already taken', 'error')
        return redirect(url_for('auth.auth_register'))
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    try:
        db.session.add(user)
        db.session.commit()
        login_user(user)
        session['user_id'] = user.id
        session['user_email'] = user.email
        flash('Registration successful! Welcome!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {e}")
        flash('Registration failed. Please try again.', 'error')
        return redirect(url_for('auth.auth_register'))

@auth_bp.route("/logout")
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Register blueprint with no prefix so /login and /register are at root
# (Do this in main.py, but here is the correct usage)
# In main.py:
# from auth import auth_bp
# app.register_blueprint(auth_bp, url_prefix='')
