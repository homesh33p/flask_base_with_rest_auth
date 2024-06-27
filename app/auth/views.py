from . import auth_bp
from . import User,AnonymousUser,db
from .forms import RegistrationForm,LoginForm
from flask import redirect,url_for,flash,render_template
from flask_login import current_user,login_user,logout_user,login_required

@auth_bp.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # if form is validated on submit gather the info and store in db, redirect to login
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))    
    return render_template("auth/register.html",form=form)

@auth_bp.route("/login",methods=['GET', 'POST'])
def login():
    # if form is validated on submit,try and load the user, if user not found flash, incorrect username or password, redirect to login,
    # if user found, verify password hash, redirect to index
    # if password hash doesnot match, redirect flash incorrect uname or password, redirect to login    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username==form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user=user)
            flash(f'{current_user.username} logged in')
            return redirect(url_for("main.index"))
        flash("incorrect username or password")
    return render_template('auth/login.html',form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    user = current_user.username
    logout_user()
    flash(f'{user} has been logged out.')
    return redirect(url_for(".login"))
