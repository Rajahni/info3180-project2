"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os, jwt
from datetime import datetime, timedelta
from functools import wraps
from app import app, db, login_manager
from flask import render_template, request, jsonify, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.models import User, Like, Post, Follow
from app.forms import UserForm, LoginForm, NewPost
from flask_wtf.csrf import generate_csrf
from flask_jwt_extended import create_access_token

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route("/api/v1/register", methods=['POST'])
def adduser():
    userform = UserForm()

    if request.method == 'POST':
    
    # Validate file upload on submit
        if userform.validate_on_submit():

            username = userform.username.data
            password = userform.password.data
            firstname = userform.firstname.data
            lastname = userform.lastname.data
            email = userform.email.data
            location = userform.location.data
            biography = userform.biography.data

            # used to store filename in database instead of photo #
            profile_photo = userform.profile_photo.data
            filename = secure_filename(profile_photo.filename)
            profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            user = User(username, password, firstname, lastname, email, location, biography, profile_photo=filename, joined_on=datetime.now())
            #                                                                                                                  #
            usersrch = db.session.execute(db.select(User).filter_by(username=user.username)).scalar()
            emailsrch = db.session.execute(db.select(User).filter_by(email=user.email)).scalar()

            if usersrch is not None:
                flash('Username already exists', 'danger')
                return jsonify(message="Username already exists")
            
            elif emailsrch is not None:
                flash('Email already exists', 'danger')
                return jsonify(message="Email already exists")
                
            elif usersrch is None:
                db.session.add(user)
                db.session.commit()
                flash('User Added', 'success')

                json_message = {"message":'New User Added Successfully',
                                "firstname":firstname,
                                "lastname":lastname,
                                "username":username,
                                "password":password,
                                "email":email,
                                "location":location,
                                "biography":biography,
                                "profile_photo":filename,
                                "joined_on":user.joined_on}
                return jsonify(json_message=json_message), 200
            
            return jsonify(errors=form_errors(userform))
    return jsonify(message="Not a POST request")

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        # userID = current_user.get_id()
        json_message = {"message":"User already logged in"}
        return jsonify(json_message)
    
    loginform = LoginForm()

    if loginform.validate_on_submit():
        # Get the username and password values from the loginform.
        username = loginform.username.data
        password = loginform.password.data
        # Using your model, query database for a user based on the username
        # and password submitted. Remember you need to compare the password hash.

        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
        
        if user is not None and check_password_hash(user.password, password):
        #if user is not None and user.password == password:
            remember_me = False

            login_user(user)

            if 'remember_me' in request.form:
                remember_me = True
            
            
            flash('Logged in successfully.', 'success')

            token = generate_token()

            json_message = {"token":token,"message": "User successfully logged in."}
            return jsonify(json_message=json_message)
        
        flash('User does not exist', 'danger')
    return jsonify(message="User does not exist"), 400

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


@app.route("/api/v1/generate-token")
def generate_token():
    timestamp = datetime.utcnow()
    payload = {
        "sub": current_user.username,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=5)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token

# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(User).filter_by(id=id)).scalar()

@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return jsonify(message="Logged out successfully"), 200
        

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

# Add new post by user
@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@login_required
def add_post(user_id):
    newpost = NewPost()

    if current_user.is_authenticated and request.method == 'POST':
        if newpost.validate_on_submit():

            caption = newpost.caption.data

            photo = newpost.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            post = Post(caption, filename, user_id, created_on=datetime.now())
            db.session.add(post)
            db.session.commit()

            json_message = {
                "message":'Successfully created a new post',
                "caption":caption,
                "photo":filename,
                "user_id":user_id,
                "created_on":post.created_on
            }
            return jsonify(json_message=json_message)
        return jsonify(errors=form_errors(newpost))

# get all posts by user    
"""@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
@login_required
def view_posts(user_id):
    if current_user.is_authenticated:
        userID = current_user.get_id()

    if request.method == 'GET':
        user = db.session.execute(db.select(User).filter_by(id=userID)).scalar()

        posts = db.session.execute(db.select(Post)).scalars()
        posts_data = []
        
        
        for post in posts:
            if int(post.user_id) == int(current_user.get_id()):
                likes = db.session.query(Post).join(Like,post.user_id==Like.user_id).count()
                posts_data.append(
                {
                    "id":post.id,
                    "user": {
                    "profile_photo": url_for('get_image', filename=user.profile_photo),
                    "username": user.username
                    },
                    "userid":post.user_id,
                    "photo":url_for('get_image', filename=post.photo),
                    "caption":post.caption,
                    "created_on":post.created_on,
                    "likes":likes
                })
        return jsonify(posts=posts_data),200"""


"""@app.route('/api/v1/users/user_id', methods=['GET'])
def get_user():
    if current_user.is_authenticated:
        user_id = current_user.get_id()

    if request.method == 'GET':
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
        posts = db.session.execute(db.select(Post).filter_by(user_id=user_id)).scalars()
        # posts = db.session.execute(db.select(Post)).scalars()
        posts_list = []

        json_user = {
            "id": user.id,
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "location": user.location,
            "biography": user.biography,
            "profile_photo": url_for('get_image', filename=user.profile_photo),
            "joined_on": user.joined_on,
            "posts":posts_list
        }

        for post in posts:
            if int(post.user_id) == int(current_user.get_id()):
                posts_list.append(
                    {
                        "id": post.id,
                        "user_id": post.user_id,
                        "photo": url_for('get_image', filename=post.photo),
                        "caption": post.caption,
                        "created_on":post.created_on,   
                    }
                )
        return jsonify(json_user)"""
    
"""@app.route('/api/users/{user_id}/follow', methods = ['POST'])
def follow(user_id):
    data = request.get_json()
    #so the follow request is in the database
    if request.method == 'POST':
         try:
             follower_id = data['follower_id']
            #  id = data['id']
            #  user_id = current_user['user_id']
             follow = Follow(user_id, follower_id)
             db.session.add(follow)
             db.session.commit()
             
             success = f"You are now following user {user_id}."
             return jsonify(message=success), 201
         except Exception as e:
           return {"Failure to add because of:": str(e)}
       
            #Flash message to indicate that an error occurred"""
                  
    
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/api/v1/posts/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.route('/api/v1/users/{user_id}', methods=['GET'])
def get_user():
    if current_user.is_authenticated:
        userID = current_user.get_id()

    if request.method == 'GET':
        user = db.session.execute(db.select(User).filter_by(id=userID)).scalar()
        posts = db.session.execute(db.select(Post)).scalars()
        posts_list = []

        json_user = {
            "id": user.id,
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "location": user.location,
            "biography": user.biography,
            "profile_photo": url_for('get_image', filename=user.profile_photo),
            "joined_on": user.joined_on,
            "posts":posts_list
        }

        for post in posts:
            if int(post.user_id) == int(current_user.get_id()):
                posts_list.append(
                    {
                        "id": post.id,
                        "user_id": post.user_id,
                        "photo": url_for('get_image', filename=post.photo),
                        "caption": post.caption,
                        "created_on":post.created_on,   
                    }
                )
        
        return jsonify(json_user=json_user)

@app.route('/api/users/<user_id>/follow', methods = ['POST'])
@login_required

def follow(user_id):
    follower_id = user.id
    #so the follow request is in the database
    if request.method == 'POST':
        try:
            user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
            if user is None:
                return jsonify({'error':'User does not exist'}), 404
            
            elif user is not None:
                # follows_list = []
                follows = db.session.execute(db.select(Follow)).scalars()
                for follow in follows:
                    print(follow.follower_id)
                    if int(follow.follower_id)==int(follower_id) and int(follow.user_id)==int(user_id):
                        return jsonify({'error':f'Already following {user.username}'})

                follow = Follow(follower_id,user_id)
                db.session.add(follow)
                db.session.commit()
                
                success = f"You are now following user {user.username}."
                return jsonify(message=success), 201
        
        except Exception as e:
            return {"Failure to add because of:": str(e)}
       
            #Flash message to indicate that an error occurred

# @app.route('/api/users/<user_id>/follow', methods=['POST'])
# @login_required
# # @requires_auth
# def follow(user_id):
#     try:
#         # Check if the user exists
#         user = User.query.filter_by(id=user_id).first()
#         if user is None:
#             return jsonify({'error': 'User not found'}), 404

#         # Add the follower and user to the Follows table
#         follow = Follow(follower_id=current_user.id, user_id=user_id)
#         db.session.add(follow)
#         db.session.commit()

#         return jsonify({'message': 'You are now following {}!'.format(user.username)}), 200
#     except:
#         return jsonify({'error': 'Unable to follow user'}), 500

@app.route('/api/v1/users/<user_id>/posts', methods=['POST','GET'])
@login_required
def posts(user_id):
    newpost = NewPost()

    if current_user.is_authenticated:
        user_id = current_user.get_id()

    if request.method == 'POST':
        if newpost.validate_on_submit():

            caption = newpost.caption.data

            photo = newpost.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #user_id = userID
            post = Post(caption, filename, user_id, created_on=datetime.now())
            db.session.add(post)
            db.session.commit()

            json_message = {
                "message":'Successfully created a new post'
                """"caption":caption,
                "photo":filename,
                "userID":user_id,
                "created_on":post.created_on"""
            }
            return jsonify(json_message=json_message)
        #return jsonify(errors=form_errors(newpost))

    if request.method == 'GET':
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()

        posts = db.session.execute(db.select(Post)).scalars()
        posts_data = []
        
        
        for post in posts:
            if int(post.user_id) == int(current_user.get_id()):
                likes = db.session.query(Post).join(Like,post.user_id==Like.user_id).count()
                posts_data.append(
                {
                    "id":post.id,
                    "user": {
                    "profile_photo": url_for('get_image', filename=user.profile_photo),
                    "username": user.username
                    },
                    "userid":post.user_id,
                    "photo":url_for('get_image', filename=post.photo),
                    "caption":post.caption,
                    "created_on":post.created_on,
                    "likes":likes
                })
        return jsonify(posts=posts_data),200


""""returns all posts for users"""
@app.route('/api/v1/posts', methods=['POST','GET'])
@login_required
def get_posts():
    if request.method == 'GET':
        posts = db.session.execute(db.select(Post)).scalars()
        posts_list = []
        for post in posts:
            likes = len(db.session.execute(db.select(Like).filter_by(id=post.id)).all())
            posts_list.append(
                {
                    "id": post.id,
                    "user_id": post.user_id,
                    "photo": url_for('get_image', filename=post.photo),
                    "caption": post.caption,
                    "created_on":post.created_on,   
                    "likes": likes
                }
                )
        return jsonify(posts=posts_list),200
    
@app.route('/api/v1/posts/<post_id>/like', methods=['POST'])
@login_required
def set_like(post_id):
    if request.method == 'POST': 
        
        isLiked = Like.query.filter(Like.post_id == post_id).filter(Like.user_id == current_user.id ).first()

        if isLiked == None: 
            like = Like(post_id, current_user.id)
            db.session.add(like)
            db.session.commit()
        else:
            json_message = {
                "message": "You already liked this post!",
                "likes": num_of_likes ,
            }
            return jsonify(json_message=json_message),400
        
        post = db.session.execute(db.select(Post).filter_by(id = post_id)).scalar()
        num_of_likes = len(db.session.execute(db.select(Like).filter_by(post_id=post.id)).all())

    
        json_message = {
            "message": "Post liked!",
            "likes": num_of_likes ,
        }

        return jsonify(json_message=json_message),201
