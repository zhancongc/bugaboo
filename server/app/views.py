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
        'name': str(int(time.time()))+'_' + img.filename,
        'date': time.strftime(config['development'].STRFTIME_FORMAT, time.localtime())
    })
    image.update({'file_path': config['development'].UPLOAD_FOLDER + image['name']})
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


