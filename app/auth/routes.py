from app.auth import auth
from flask import render_template, redirect, url_for, flash, request
from app.auth.forms import RegistrationForm, LoginForm, UpdateAccount, ResetPassword, ResetPasswordForm #import the account form to route <- updateaccount
from app import bcrypt, db
from app.auth.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.auth.utils import save_picture, send_reset_email


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in", 'warning')
        return redirect(url_for("posts.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username= username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Cool, you're done. {}" .format(username), 'success')
        return redirect(url_for('auth.login'))
    return render_template("register.html", reg_form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", 'alert')
        return redirect(url_for("posts.home"))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        password = login_form.password.data
        email = login_form.email.data
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=login_form.remember.data)
            flash("Logged in successfully", 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('posts.home'))
            return redirect(url_for('posts.home'))
            # return redirect(next_page) if next_page else redirect(url_for('posts.home'))
        else:
            flash("Wrong credentials", 'danger')
    return render_template("login.html", log_form = login_form)

@auth.route("/logout")
def signout():
    logout_user()
    return redirect(url_for('posts.home'))


@auth.route("/account", methods=["GET", "POST"])
@login_required #decorator here
def account():
    #instantiate
    form = UpdateAccount()
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    elif form.validate_on_submit():
        pic_data = form.picture.data
        if pic_data:
            profile_picture = save_picture(pic_data)
            current_user.img_file = profile_picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account has been updated!!!!!", "success")
        return redirect(url_for("auth.account"))


    return render_template('account.html', update_form=form) #update_form is for html and equals to form here


@auth.route("/reset-request", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))

    form = ResetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)

        flash("The Email has been sent! Please check your inbox and reset your password.", 'info')
        redirect (url_for('auth.login'))
    return render_template('reset_request.html', form = form)

@auth.route('/reset-password/<token>', methods=["GET","POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('The Link has been expired, make a new request', 'warning')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user.password = hashed_password
        db.session.commit()
        flash("The password has been changed.", "success")
    return render_template('reset_password.html', form=form)
