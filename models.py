"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """create User instances"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    image_url = db.Column(db.Text, nullable = False, default="/static/default-pic.png")

    def __rep__(self):
        """Show info about user"""

        return f'<User {self.id}{self.first_name}{self.last_name}{self.image_url}>'
     
