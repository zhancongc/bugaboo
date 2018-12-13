import time
import datetime
import hashlib
from app import app, db
from flask import jsonify, request, render_template
from .package import wxlogin
from .models import User, UserInfo
from config import configs


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in configs['development'].PICTURE_ALLOWED_EXTENSIONS


@app.route('/')
def index():
    print('index')
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    res = dict()
    code = request.values.get('code')
    if code is None:
        res.update({
            'state': 0,
            'msg': 'None code'
        })
        return jsonify(res)
    try:
        wx = wxlogin(code)
    except Exception:
        res.update({
            'state': 0,
            'msg': 'get user info from weixin server error'
        })
        return jsonify(res)
    open_id = wx.get('openid')
    union_id = wx.get('unionid')
    session_key = wx.get('session_key')
    if open_id is None or union_id is None or session_key is None:
        res.update({
            'state': 0,
            'msg': 'cannot find user info'
        })
        return jsonify(res)
    user = User.query.get_or_404(union_id)
    if user:
        current_time = datetime.datetime.utcnow()
        user.login_time = current_time.strftime(configs['development'].STRFTIME_FORMAT)
        user.session_id_expire_time = (current_time + datetime.timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
        user.session_key = session_key
        sh = hashlib.sha1()
        sh.update(session_key.encode())
        sh.update(configs['development'].APPLICATION_SECRET)
        user.session_id = sh.hexdigest()

    else:
        user = User()
        #user = User(avatarUrl=wx.get('avatarUrl'), city=wx.get('city'),
        #            country=wx.get('country'), gender=wx.get('gender'), language=wx.get('language'),
        #            nickName=wx.get('nickName'), province=wx.get('province'), login_time=wx.get('login_time'))
        db.session.add(user)
        db.session.commit()
    res.update({
        'state': 1,
        'msg': '',
        'data': 'session_key'
    })
    return jsonify({'login': True, 'open_id': open_id})


@app.route('/upload', methods=['POST'])
def upload():
    res = dict()
    img = request.files.get('composition')
    if not img:
        res.update({
            'state': 0,
            'msg': 'None file'
        })
        return jsonify(res)
    if not allowed_file(img.filename):
        res.update({
            'state': 0,
            'msg': 'Wrong file format'
        })
        return jsonify(res)
    if img.filename == '':
        res.update({
            'state': 0,
            'msg': 'No selected file'
        })
        return jsonify(res)
    image = dict()
    image.update({
        'name': str(int(time.mktime(time.gmtime())))+'_' + img.filename,
        'date': datetime.datetime.utcnow().strftime(configs['development'].STRFTIME_FORMAT)
    })
    image.update({'file_path': configs['development'].UPLOAD_FOLDER + image['name']})
    try:
        img.save(image['file_path'])
    except Exception as e:
        res.update({
            'state': 0,
            'msg': 'Error occurred while saving file'
        })
        print(e)
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'Upload success',
        'data': image
    })
    return jsonify(res)


