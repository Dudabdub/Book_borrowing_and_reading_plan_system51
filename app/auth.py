from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, login
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('auth', __name__, template_folder='templates')

@bp.route('/register', methods=['GET','POST']) 
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('请完整填写表单', 'warning')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'warning')
            return redirect(url_for('auth.register'))
        u = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and check_password_hash(u.password_hash, password):
            login_user(u)
            return redirect(url_for('main.index'))
        flash('登录失败，检查邮箱和密码', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
