from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



def connect_db(app):
    with app.app_context():
        db.init_app(app)

default_url = 'https://images.rawpixel.com/image_png_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTAxL3JtNjA5LXNvbGlkaWNvbi13LTAwMi1wLnBuZw.png'

#    Model down here

class Blog(db.Model):

    __tablename__ = 'bloggers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(25), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    image_url = db.Column(db.String(300), nullable=False, default='default_url')

    posts = db.relationship('Post', backref='blogger')

    def __repr__(self):
        """show info about post"""
        p = self 
        return f'<Pet id ={p.id} first name ={p.first_name} last name ={p.last_name} img ={p.image_url}'
    
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"



class Post(db.Model):
    '''model for user's blog post'''

    __tablename__  = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(25), nullable=False)

    content = db.Column(db.String(3000), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False,default=datetime.now)

    blogger_id = db.Column(db.Integer, db.ForeignKey('bloggers.id'))

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    

class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )
