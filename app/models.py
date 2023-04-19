from . import db
from werkzeug.security import generate_password_hash
# Add any model classes for Flask-SQLAlchemy here

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String)
    photo = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # attempt at creating a foreign key
    created_on = db.Column(db.DateTime)

    def __init__(self, caption, photo, user_id, created_on):
        self.caption = caption
        self.photo = photo
        self.user_id = user_id
        self.created_on = created_on
    
    def __repr__(self):
        return f'<Post %r {self.id}>'

class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # post = db.relationship("Post", backref=db.backref("posts", uselist=False))

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id
        
    def __repr__(self):
        return f'<Like %r {self.id}>'
    
class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # post = db.relationship("Post", backref=db.backref("posts", uselist=False))

    def __init__(self, follower_id, user_id):
        self.follower_id = follower_id
        self.user_id = user_id
        
    def __repr__(self):
        return f'<Follow %r {self.id}>'
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    location = db.Column(db.String)
    biography = db.Column(db.String)
    profile_photo = db.Column(db.String)
    joined_on = db.Column(db.DateTime)

    post = db.relationship("Post", backref="posts", lazy=True)
    like = db.relationship("Like", backref="likes", lazy=True)
    follow = db.relationship("Follow", backref="follows", lazy=True)

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo, joined_on):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo
        self.joined_on = joined_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
    def __repr__(self):
        return f'<User %r {self.id}>'