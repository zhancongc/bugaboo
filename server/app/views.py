from app import app, db
from flask import jsonify, request
from .package import wxlogin
from .models import User


@app.route("/test")
def index():
    return "Hello, World!"


@app.route('/login', methods=['POST'])
def login():
    code = request.values.get('code')
    if code is None:
        return jsonify({'login': False})
    openid = wxlogin(code).get('openid')
    # out_log('openid'+('None' if openid is None else openid))
    if openid is None:
        return jsonify({'login': False})
    db = get_db()
    if db.user.find({'openid': openid}).count() > 1:
        db.user.remove({'openid': openid}, multi=True)
        db.user.insert({'openid': openid, 'login_time': time.time()})
    else:
        db.user.update({'openid': openid}, {'$set': {'login_time': time.time()}}, upsert=True)
    return jsonify({'login': True, 'openid': openid})


@app.route('/login', methods=['POST'])
def login():
    code = request.values.get('code')
    if code is None:
        return jsonify({'login': False})
    open_id = wxlogin(code).get('open_id')
    if open_id is None:
        return jsonify({'login': False})
    if User.query.get_or_404(open_id):
        
    if db.user.find({'openid': openid}).count() > 1:
        db.user.remove({'openid': openid}, multi=True)
        db.user.insert({'openid': openid, 'login_time': time.time()})
    else:
        db.user.update({'openid': openid}, {'$set': {'login_time': time.time()}}, upsert=True)
    return jsonify({'login': True, 'openid': openid})

