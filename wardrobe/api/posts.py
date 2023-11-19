"""REST API for wardrobe."""

import hashlib
import flask
import wardrobe
import os


def get_most_recent_clothesid(logname):
    """Return most recent clothesid by user"""
    connection = wardrobe.model.get_db()
    cur = connection.execute(
        """
        SELECT clothing.clothesid
        FROM clothing
        WHERE clothing.owner = ? 
        ORDER BY clothing.clothesid DESC
        LIMIT 1
        """,
        (logname,),
    )
    m_r = cur.fetchone()
    if m_r:
        return m_r['clothesid']
    return 0


def not_logged():
    """Return 403 if user is not logged in."""
    print("WE AINT LOGGED IN!")
    context1 = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**context1), 403


def verify_pass(password, storedhash):
    """Wardrobe check if password matches."""
    algo, salt2, passhash = storedhash.split('$')
    hash_obj58 = hashlib.new(algo)
    saltedpass = salt2 + password
    hash_obj58.update(saltedpass.encode('utf-8'))
    print(passhash)
    print(hash_obj58.hexdigest())
    return passhash == hash_obj58.hexdigest()


def check_logged():
    """Check if user is logged in."""
    logname = flask.session.get('username')
    if 'username' not in flask.session:
        auth = flask.request.authorization
        if auth is not None and 'username' in auth and 'password' in auth:
            username = flask.request.authorization['username']
            password = flask.request.authorization['password']
        else:
            return "notloggedin"
        connection = wardrobe.model.get_db()
        if not username or not password:
            return "notloggedin"
        cur = connection.execute(
            """
            SELECT username, password FROM users WHERE username = ?
            """,
            (username,),
        )
        user = cur.fetchone()
        if user and verify_pass(password, user['password']):
            flask.session['username'] = user['username']
            logname = user['username']
        else:
            return "notloggedin"
    return logname


@wardrobe.app.route('/api/v1/', methods=["GET"])
def get_api():
    """Return API services."""
    context = {
        "clothes": "/api/v1/clothes/",
        "url": flask.request.path,
    }
    return flask.jsonify(**context)


@wardrobe.app.route('/api/v1/clothing/', methods=["GET"])
def get_clothing():
    """Return the clothes stored on the logged-in user's account."""
    logname = check_logged()
    if logname == "notloggedin":
        print("NOT LOGGED IN")
        return not_logged()
    
    size = flask.request.args.get('size', default=12, type=int)
    page = flask.request.args.get('page', default=0, type=int)
    m_r = get_most_recent_clothesid(logname)
    clothesid_lte = flask.request.args.get('clothesid_lte', default=m_r, type=int)
    newp2 = flask.request.full_path
    if newp2.endswith('?'):
        newp2 = newp2[:-1]
    if size <= 0 or page < 0 or (clothesid_lte is not None and clothesid_lte < 0):
        context = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(**context), 400

    connection = wardrobe.model.get_db()
    cur = connection.execute(
        """
        SELECT clothing.clothesid, clothing.filename, clothing.owner, 
        clothing.article, clothing.confidence
        FROM clothing
        WHERE clothing.owner = ?
        AND (clothing.clothesid <= ? OR ? IS NULL)
        ORDER BY clothing.clothesid DESC
        LIMIT ? OFFSET ?
        """,
        (logname, clothesid_lte, clothesid_lte, size, page * size),
    )
    clothes_data = cur.fetchall()
    
    next_page_url = ""
    if len(clothes_data) >= size:
        npu = "/api/v1/clothing/?size={}&page={}&clothesid_lte={}"
        next_page_url = npu.format(size, page + 1, clothesid_lte)
    response = {
        "next": next_page_url,
        "results": [
            {
                "clothesid": clothing['clothesid'],
                "filename": "/uploads/" + clothing['filename'],
                "owner": clothing['owner'],
                "article": clothing['article'],
                "confidence": clothing['confidence'],
                "url": f"/api/v1/clothing/{clothing['clothesid']}/"
            }
            for clothing in clothes_data
        ],
        "url": newp2,
    }
    return flask.jsonify(**response)


@wardrobe.app.route('/api/v1/prompt/', methods=["POST"])
def prompt_to_output():
    logname = check_logged()
    data = flask.request.json
    prompt = data.get('inputData')
    
    # Get prompt input
    
    # Get all articles from DB
    connection = wardrobe.model.get_db()
    cur = connection.execute(
        """
        SELECT clothing.article
        FROM clothing
        WHERE clothing.owner = ?
        ORDER BY clothing.clothesid DESC;
        """,
        (logname,),
    )
    dats2 = cur.fetchall()
    # print(prompt)
    # print(dats2)
    # Combine articles + prompt input into GPT submission

    # Receive GPT output

    # Parse GPT output

    # GET JSON which is a list of fileImages.

    # Send JSON of outfit back to React side!



    image_files = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        # ... more image URLs
    ]
    response_data = {
            "imageFiles": image_files
        }
    return flask.jsonify(response_data), 200






