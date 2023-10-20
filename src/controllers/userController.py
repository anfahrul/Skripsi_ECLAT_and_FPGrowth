from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from flask_login import login_user, current_user
from src.models.user import User


def getProfile():
    user = User.query.filter_by(email=current_user.email).first()
    
    return render_template('user/profile.html', user=user)


def editProfile(user_id):
    user = User.query.get(user_id)
    
    return render_template('user/edit_profile.html', user=user)


def updateProfile(user_id):
    request_form = request.form.to_dict()
    user = User.query.get(user_id)
    
    user.name = request_form['name']

    db.session.commit()
    
    flash('Profil berhasil diperbarui!')
    return redirect(url_for('user_blueprint.profile'))


def updatePassword(bcrypt):
    user = User.query.filter_by(email=current_user.email).first()
    request_form = request.form.to_dict()
    
    old_password = request_form['old_password']
    new_password = request_form['new_password']
    
    if not user or not bcrypt.check_password_hash(user.password, old_password):
        flash('Kata sandi lama yang anda masukkan salah!')
        
    password_hashed = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = password_hashed
    
    db.session.commit()
    
    flash('Kata sandi berhasil diperbarui!')
    return render_template('user/profile.html', user=user)