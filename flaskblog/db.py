from datetime import datetime
from flaskblog import database, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(60), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    post = database.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    date_posted = database.Column(database.DateTime(100), nullable=False, default=datetime.utcnow)
    content = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"


# database.create_all()

# user_1 = User(username="Eddie", email="spaghettilb@icloud.com", password="password")
# database.session.add(user_1)
# database.session.commit()

# database.drop_all()
# print(User.query.all())
# user = User.query.first()
# print(user.password)
# User.query.all()
