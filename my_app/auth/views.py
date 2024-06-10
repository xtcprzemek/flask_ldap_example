import ldap
from flask import request, render_template, flash, redirect, url_for, Blueprint, g
from flask_login import current_user, login_user, \
    logout_user, login_required
from my_app import login_manager
from my_app.auth.models import User, ldap_login
from my_app.auth.forms import LoginForm
from contextlib import suppress

auth = Blueprint('auth', __name__)
 
users=set()

@login_manager.user_loader
def load_user(id):
    print(f'user_loader->users: {users}')
    print(f'user_loader->id: {id}')
    u = [user for user in users if user.id == id ]
    if len(u)>0:
        return u[0]
    return None


@auth.before_request
def get_current_user():
    g.user = current_user
 
 
@auth.route('/')
@auth.route('/home')
def home():
    print(f'home->users: {users}')
    print(f'home->current_user: {current_user}')
    return render_template('home.html', current_user=current_user)
 
 
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('auth.home'))
 
    form = LoginForm(request.form)
 
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
 
        try:
            ret = ldap_login(username, password)
            #User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('login.html', form=form)
        user = User(ret)
        users.add(user)
        
        
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('auth.home'))
 
    if form.errors:
        flash(form.errors, 'danger')
 
    return render_template('login.html', form=form)
 
 
@auth.route('/logout')
@login_required
def logout():
    users.remove(current_user)
    logout_user()
    
    return redirect(url_for('auth.home'))

@auth.route('/hidden')
@login_required
def hidden():
    return f'this content is visible only for logged user.<BR> You are logged as {current_user.name}'