"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


default_image = "https://www.lococrossfit.com/wp-content/uploads/2019/02/user-icon.png"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(20),
                           nullable=False,
                           )

    last_name = db.Column(db.String(30),
                          nullable=False)

    image_url = db.Column(db.Text,
                          default=default_image)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
