"""REST API for wardrobe."""

import hashlib
import flask
import wardrobe


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
        (logname, logname),
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
    """Return the clothes stored on logged in users account."""
    logname = check_logged()
    if logname == "notloggedin":
        print("NOT LOGGED IN")
        return not_logged()
    size = flask.request.args.get('size', default=10, type=int)
    page = flask.request.args.get('page', default=0, type=int)
    m_r = get_most_recent_clothesid(logname)
    clothesid_lte = flask.request.args.get('clothesid_lte', default=m_r, type=int)
    newp2 = flask.request.full_path
    if newp2.endswith('?'):
        newp2 = newp2[:-1]
    if size <= 0 or page < 0 or clothesid_lte < 0:
        context = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(**context), 400
    connection = wardrobe.model.get_db()
    cur = connection.execute(
        """
        SELECT clothing.clothesid
        FROM clothing
        INNER JOIN users ON clothing.owner = users.username
        WHERE clothing.owner = ?
        AND clothing.clothesid <= ?
        ORDER BY clothing.clothesid DESC
        LIMIT ? OFFSET ?
        """,
        (logname, logname, clothesid_lte, size, page * size),
    )
    clothes_ids = cur.fetchall()
    next_page_url = ""
    if len(clothes_ids) >= size:
        npu = "/api/v1/clothing/?size={}&page={}&clothesid_lte={}"
        next_page_url = npu.format(size, page + 1, clothesid_lte)
    response = {
        "next": next_page_url,
        "results": [
            {"clothesid": clothes_id['clothesid'],
             "url": f"/api/v1/clothing/{clothes_id['clothesid']}/"}
            for clothes_id in clothes_ids
        ],
        "url": newp2,
    }
    return flask.jsonify(**response)


@wardrobe.app.route('/api/v1/clothes/<int:clothesid_url_slug>/', methods=["GET"])
def get_cloth(clothesid_url_slug):
    """Return details of cloth from clothesid."""
    logname = check_logged()
    if logname == "notloggedin":
        print("NOT LOGGED IN")
        return not_logged()
    print("ACCOUNT IS LOGGED IN")
    # KEEP ABOVE FOR EVERY FUNCTION!
    connection = wardrobe.model.get_db()
    # Check if the cloth with clothesid exists
    cur = connection.execute(
        """
        SELECT *
        FROM clothing
        WHERE clothesid = ?
        """,
        (clothesid_url_slug,),
    )
    cloth4 = cur.fetchone()
    if cloth4 is None:
        context4 = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(**context4), 404
    cur = connection.execute(
        """
        RETURN ATTRIBUTES OF CLOTHING
        """,
        (clothesid_url_slug,),
    )
    clothes_data = cur.fetchone()
    clothes = {
        "owner": clothes_data["owner"],
        "filename": clothes_data["filename"],
        "article": clothes_data["article"],
        "confidence": clothes_data["confidence"],
        "clothesid": clothesid_url_slug,
        "url": f"/api/v1/clothes/{clothesid_url_slug}/",
    }
    return flask.jsonify(**clothes)
