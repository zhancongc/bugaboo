import time
from app import app, db
from flask import jsonify, request, render_template
from .package import wxlogin
from .models import User
from config import configs


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in configs['development'].PICTURE_ALLOWED_EXTENSIONS


@app.route('/')
def index():
    print('index')
    return render_template('index.html')


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


@app.route('/upload', methods=['POST'])
def upload():
    res = dict()
    img = request.files.get('composition')
    if allowed_file(img.filename):
        image = dict()
        image.update({
            'name': str(int(time.time()))+'_' + img.filename,
            'date': time.strftime(configs['development'].STRFTIME_FORMAT, time.localtime())
        })
        image.update({'file_path': configs['development'].UPLOAD_FOLDER + image['name']})
        img.save(image['file_path'])
        res.update({
            'state': 1,
            'msg': 'upload success',
            'data': image
        })
    else:
        res.update({
            'state': 0,
            'msg': 'file format is not supported'
        })
    return jsonify(res)


