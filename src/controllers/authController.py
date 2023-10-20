from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from flask_login import login_user
from src.models.user import User


def registerPost(bcrypt):
    request_form = request.form.to_dict()
    
    name = request_form['name']
    email = request_form['email']
    password = request_form['password']
    
    user = User.query.filter_by(email=email).first()
    
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email telah terdaftar dalam sistem!')
        return redirect(url_for('auth_blueprint.register'))
    
    new_user = User(
        email=email,
        name=name,
        password=bcrypt.generate_password_hash(password).decode('utf-8'),
        created_at=datetime.now())
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth_blueprint.login'))


def loginPost(bcrypt):
    request_form = request.form.to_dict()
    
    email = request_form['email']
    password = request_form['password']
    remember = True if request_form['remember'] else False
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        flash('Email atau kata sandi salah!')
        return redirect(url_for('auth_blueprint.login'))

    login_user(user, remember=remember)
    return redirect(url_for('dashboard_blueprint.dashboard'))