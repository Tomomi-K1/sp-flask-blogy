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

    tags=db.relationship('Tag', secondary ='posttags', backref='posts')

    middletable=db.relationship('PostTag', backref='posttable', cascade="all, delete")

    def __repr__(self):
        """Show info about post"""

        return f'<post {self.id} {self.title}>'


class Tag(db.Model):
    """create tag instances"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique = True)
    
    def __repr__(self):
        """Show info about Tag"""

        return f'<tag {self.id} {self.name}>'


class PostTag(db.Model):

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        """Show info about posttag"""

        return f'<posttags {self.post_id} {self.tag_id}>'