"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# =======springboard solution======
# DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    """Connect this database to provided Flask app. connect_db(app) is used in app.py """
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

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    # this relationship needs to be create under User since it's one to many relationship. if you want to do delete-orphan, you have to set relationship on "one" side of table
    # delete-orphan cascade adds behavior to the delete cascade, such that a child object will be marked for deletion when it is de-associated from the parent, not just when the parent is marked for deletion.


    # =======springboard solution======

    # @property
    # def full_name(self):
    #     """Return full name of user."""

    #     return f"{self.first_name} {self.last_name}"
     
class Post(db.Model):
    """ create post instances"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(1000), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship('User', backref='posts', cascade="all, delete-orphan")
    # need to put cascade="all, delete-orphen" otherwise when deleting user, post won't be del

    tags=db.relationship('Tag', secondary ='posttags', backref='posts')

    middletable=db.relationship('PostTag', backref='posttable', cascade="all, delete")

    def __repr__(self):
        """Show info about post"""

        return f'<post {self.id} {self.title}>'

    # =======springboard solution======
    # @property
    # def friendly_date(self):
    #     """Return nicely-formatted date."""

    #     return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
    """create tag instances"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique = True)
    
    def __repr__(self):
        """Show info about Tag"""

        return f'<tag {self.id} {self.name}>'


class PostTag(db.Model):
    """ Tag and post relationship table"""

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
    # ===springboard solution=====
    # post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    # tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    # ????why don't I need to put ondelete=cascade?????

    def __repr__(self):
        """Show info about posttag"""

        return f'<posttags {self.post_id} {self.tag_id}>'