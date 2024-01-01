from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
import datetime
db=SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)



"""Models for Blogly."""
#class will be mapped to a table
class User(db.Model):
    __tablename__ = "users"
    #columns of table are class attributes; specify datatypes and constraints
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(20),
                           nullable=False)
    last_name = db.Column(db.String(20),
                          nullable=False)
    #default image?
    picture = db.Column(db.Text,
                          nullable=False)
    #set reference to Post class and access attributes via "user"
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.picture}>"

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.TEXT)
    post = db.Column(db.TEXT)
    created_at = db.Column(db.TIMESTAMP,
                             default=datetime.datetime.now)
    #use table_name, not model name
    user_id =db.Column(db.Integer, 
                      db.ForeignKey('users.id'),
                      nullable=False)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    posts = db.relationship('Post', secondary="post_tags", backref="tags")


class PostTag(db.Model):
    __tablename__ = 'post_tags'
    #need to make sure combination of these two is unique.  How?
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
                       
   