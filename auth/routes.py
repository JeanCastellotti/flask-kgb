from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_user, login_required, logout_user
from app import bcrypt
from .forms import LoginForm
from models import Admin

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password,
                                                form.password.data):
            login_user(admin, remember=True)
            next_page = request.args.get('next')
            flash('Vous êtes connecté.', 'success')
            if next_page: return redirect(next_page)
            return redirect(url_for('admin.missions'))
        flash('Vos identifiants sont incorrects.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous êtes déconnecté.', 'success')
    return redirect(url_for('auth.login'))
