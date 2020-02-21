import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, database, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, AccountUpdateForm, PostForm
from flaskblog.db import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home_page():
    posts = Post.query.all()
    return render_template("home_page.html", posts=posts)


@app.route('/about')
def about_page():
    return render_template("about_page.html")


@app.route('/registration', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        database.session.add(user)
        database.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home_page"))
        else:
            flash("Login Unsuccessful. Please check username and password!", "danger")
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        database.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", image_file=image_file, form=form)


@app.route('/post/new', methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("home_page"))
    return render_template("create_post.html", form=form)


@app.route('/post/<int:post_id>', methods=["GET", "POST"])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("view_post.html", post=post)