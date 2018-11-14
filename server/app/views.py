import time
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
    wx = wxlogin(code)
    open_id = wx.get('openid')
    if open_id is None:
        return jsonify({'login': False})
    user = User.query.get_or_404(open_id)
    if user:
        user.login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    else:
        user = User(user_id=None, open_id=open_id, avatarUrl=wx.get('avatarUrl'), city=wx.get('city'),
                    country=wx.get('country'), gender=wx.get('gender'), language=wx.get('language'),
                    nickName=wx.get('nickName'), province=wx.get('province'), login_time=wx.get('login_time'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'login': True, 'open_id': open_id})

