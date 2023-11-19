"""
Wardrobe index (main) view.

URLs include:
/
"""
import os
import uuid
import hashlib
import pathlib
import flask
import arrow
import wardrobe
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib

def get_user_info(connection, username):
    """B ALL user info from username."""
    cur = connection.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,),
    )
    return cur.fetchone()


@wardrobe.app.route('/')
def show_index():
    """Wardrobe Index Page!."""
    logname = flask.session.get('username')
    print(logname)
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    # bug fixing
    connection = wardrobe.model.get_db()
    uinf = get_user_info(connection, logname)
    if uinf is None:
        flask.session.clear()
        return flask.redirect(flask.url_for('show_login'))
    context = {"logname": logname}
    return flask.render_template("index.html", **context)


@wardrobe.app.route('/accounts/login/', methods=["GET"])
def show_login():
    """Wardrobe login."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template("login.html")


@wardrobe.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Wardrobe logout."""
    flask.session.clear()
    return flask.redirect(flask.url_for('show_login'))


@wardrobe.app.route('/accounts/create/', methods=['GET'])
def create_account():
    """Wardrobe create account."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('edit_account'))
    return flask.render_template("create.html")


@wardrobe.app.route('/users/<user_url_slug>/')
def show_user(user_url_slug):
    """User profile/view others? page."""
    # GET LOG NAME AND REDIRECT TO LOGIN IF NOT LOGGED IN!!
    logname = flask.session.get('username')
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    if logname != user_url_slug:
        # causes users to not be able to look at other peoples clothes
        return flask.redirect(flask.url_for('show_index'))
    connection = wardrobe.model.get_db()
    user_info = get_user_info(connection, user_url_slug)
    if user_info is None:
        flask.abort(404)
    context = {
        "user_info": user_info,
        "logname": logname,
    }
    return flask.render_template("user.html", **context)


@wardrobe.app.route('/accounts/delete/', methods=['GET'])
def delete_account_confirmation():
    """Wardrobe delete account."""
    logname = flask.session.get('username')
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    return flask.render_template("delete_confirmation.html", logname=logname)


@wardrobe.app.route('/accounts/edit/', methods=['GET'])
def edit_account():
    """Wardrobe edit profile."""
    logname = flask.session.get('username')
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    # Get user's current photo, name, and email from the database
    connection = wardrobe.model.get_db()
    user_info = get_user_info(connection, logname)
    # Render the edit account page with user information
    context = {
        "logname": logname,
        "fullname": user_info["fullname"],
        "email": user_info["email"],
        "profile_picture": user_info["filename"],
    }
    return flask.render_template("edit.html", **context)


@wardrobe.app.route('/accounts/password/', methods=['GET'])
def edit_password():
    """Wardrobe edit password."""
    # GET LOG NAME AND REDIRECT TO LOGIN IF NOT LOGGED IN!!
    logname = flask.session.get('username')
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    return flask.render_template("edit_password.html", logname=logname)


@wardrobe.app.route('/accounts/auth/')
def check_auth():
    """Wardrobe authenticate user."""
    # GET LOG NAME AND REDIRECT TO LOGIN IF NOT LOGGED IN!!
    if 'username' not in flask.session:
        return flask.abort(403)
    return ('', 200)


def user_exists(connection, username):
    """Wardrobe check if user exists already."""
    cur = connection.execute(
        """
        SELECT 1
        FROM users
        WHERE username = ?
        """,
        (username,),
    )
    return cur.fetchone() is not None


def check_pass(password, storedhash):
    """Check if password is same as hash."""
    algo, salt, passhash = storedhash.split('$')
    hash_obj = hashlib.new(algo)
    saltedpass = salt + password
    hash_obj.update(saltedpass.encode('utf-8'))
    print(passhash)
    print(hash_obj.hexdigest())
    return passhash == hash_obj.hexdigest()


def hash_password(password):
    """Hash password"""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def del_file(filename):
    """Delete PFP from filename."""
    photo_path = os.path.join(wardrobe.app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(photo_path):
        os.remove(photo_path)


@wardrobe.app.route('/accounts/', methods=['POST'])
def account():
    """B DOCSTIRNG MOMENT."""
    logname = flask.session.get('username')
    operation = flask.request.form.get('operation')
    redirection = flask.request.args.get('target', '/')
    connection = wardrobe.model.get_db()
    if operation == "login":
        login_user(connection)
    elif operation == "create":
        create_user(connection)
    elif operation == "delete":
        delete_user(connection, logname)
    elif operation == "edit_account":
        edit_user_account(connection, logname)
    elif operation == "update_password":
        update_password(connection, logname)
    return flask.redirect(redirection)


def login_user(connection):
    """Login user."""
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if not username or not password:
        flask.abort(400)
    cur = connection.execute(
        """
        SELECT username, password FROM users WHERE username = ?
        """,
        (username,),
    )
    user = cur.fetchone()
    if user and check_pass(password, user['password']):
        flask.session['username'] = user['username']
    else:
        flask.abort(403)


def create_user(connection):
    """Create user."""
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')
    file = flask.request.files.get('file')
    hold = password
    if not username or not hold or not fullname or not email or not file:
        flask.abort(400)
    if user_exists(connection, username):
        flask.abort(409)
    newpass = hash_password(password)
    fileobj = file
    filename = fileobj.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    if not fileobj:
        flask.abort(400)
    path = wardrobe.app.config["UPLOAD_FOLDER"] / uuid_basename
    fileobj.save(path)
    connection.execute(
        """
        INSERT INTO users (username, password, fullname, email, filename)
        VALUES (?, ?, ?, ?, ?)
        """,
        (username, newpass, fullname, email, uuid_basename),
    )
    connection.commit()
    flask.session['username'] = username


def delete_user(connection, logname):
    """Delete user from name"""
    if 'username' not in flask.session:
        flask.abort(403)
    usrposts = get_user_posts(connection, logname)
    for post in usrposts:
        del_file(post['filename'])
    del_file(get_user_info(connection, logname)['filename'])
    connection.execute(
        """
        DELETE FROM users WHERE username = ?
        """,
        (logname,),
    )
    connection.commit()
    flask.session.clear()


def edit_user_account(connection, logname):
    """Edit form for user's account."""
    if 'username' not in flask.session:
        flask.abort(403)
    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')
    file = flask.request.files.get('file')
    if not fullname or not email:
        flask.abort(400)
    if file:
        del_file(get_user_info(connection, logname)['filename'])
        fileobj = file
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        if not fileobj:
            flask.abort(400)
        path = wardrobe.app.config["UPLOAD_FOLDER"] / uuid_basename
        fileobj.save(path)
        connection.execute(
            """
            UPDATE users SET fullname = ?, email = ?, filename = ?
            WHERE username = ?
            """,
            (fullname, email, uuid_basename, logname),
        )
        connection.commit()
    else:
        connection.execute(
            """
            UPDATE users SET fullname = ?, email = ?
            WHERE username = ?
            """,
            (fullname, email, logname),
        )
        connection.commit()


@wardrobe.app.route('/test/')
def upload_clothes():

    """Upload clothes"""
    #image_filename = flask.request.form.get('image_upload')
    img = flask.url_for('static', filename='images/clothes')
    img_height = 96
    img_width = 96
    # verify logged in user
    model = tf.keras.models.load_model('my_model_RMSprop.keras')
    new_image_path = pathlib.Path('./TestImages/IMG_3150').with_suffix('.jpg')
    img = tf.keras.utils.load_img(
    new_image_path, target_size=(img_height, img_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['black_dress', 'black_pants', 'black_shirt', 'black_shoes', 'black_shorts', 'black_suit', 'blue_dress', 'blue_pants', 'blue_shirt', 'blue_shoes', 'blue_shorts', 'brown_hoodie', 'brown_pants', 'brown_shoes', 'green_pants', 'green_shirt', 'green_shoes', 'green_shorts', 'green_suit', 'pink_hoodie', 'pink_pants', 'pink_skirt', 'red_dress', 'red_hoodie', 'red_pants', 'red_shirt', 'red_shoes', 'silver_shoes', 'silver_skirt', 'white_dress', 'white_pants', 'white_shoes', 'white_shorts', 'white_suit', 'yellow_dress', 'yellow_shorts', 'yellow_skirt']
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )






def update_password(connection, logname):
    """Update password"""
    op1 = flask.request.form.get('password')
    new_password1 = flask.request.form.get('new_password1')
    new_password2 = flask.request.form.get('new_password2')
    if not op1 or not new_password1 or not new_password2:
        flask.abort(400)
    if not check_pass(op1, get_user_info(connection, logname)['password']):
        flask.abort(403)
    if new_password1 != new_password2:
        flask.abort(401)
    newhash = hash_password(new_password1)
    connection.execute(
        """
        UPDATE users SET password = ? WHERE username = ?
        """,
        (newhash, logname,),
    )
