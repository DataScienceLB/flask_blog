from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

application = app = Flask(__name__)
app.config["SECRET_KEY"] = "f2f952daaf55e753e43849f39da04c3d"

posts = [
    {
        'author': 'Eduardo Licea',
        'title': 'Learning to blog',
        'content': 'Having fun coding a blog in python.',
        'date_posted': 'February 13, 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'Learning to flask',
        'content': 'I love flask.',
        'date_posted': 'February 13, 2020'
    }
]


@app.route('/')
def home_page():
    class startup():
        def __init__(self):
            pass

    return render_template("home_page.html", posts=posts)


@app.route('/about')
def about_page():
    return render_template("about_page.html")


@app.route('/registration', methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home_page"))
    return render_template("register.html", form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
