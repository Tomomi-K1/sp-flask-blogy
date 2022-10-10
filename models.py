"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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


    def __repr__(self):
        """Show info about user"""

        return f'<User {self.id} {self.first_name} {self.last_name} {self.image_url}>'
     
class Post(db.Model):
    """ create post instances"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(1000), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')


    def __repr__(self):
        """Show info about user"""

        return f'<post {self.id} {self.title}>'