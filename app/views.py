"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os, datetime
from app import app, db, login_manager
from flask import render_template, request, jsonify, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.models import User, Like, Post, Follow
from app.forms import UserForm


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

app.route('/api/v1/register', methods=['POST'])
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

            user = User(username, password, firstname, lastname, email, location, biography, joined_on=datetime.datetime.now())
            #                                                                                                                  #
            usersrch = db.session.execute(db.select(User).filter_by(username=user.username)).scalar()

            if usersrch is not None:
                flash('Username already exists', 'danger')
            elif usersrch is None:
                usersrch = db.session.execute(db.select(User).filter_by(username=user.username)).scalar()


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