import time
import datetime
from app import app, db
from flask import jsonify, request, render_template
from .package import wxlogin, get_sha1
from .models import User, UserInfo
from config import configs


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in configs['development'].PICTURE_ALLOWED_EXTENSIONS


def check_session_id(session_id):
    """
    :function: 检查用户登录状态是否失效
    :param session_id: session_id
    :return:
    """
    user = User.query.get_or_404(session_id)
    if user:
        current = datetime.datetime.utcnow()
        expire = datetime.datetime.strptime(user.session_id_expire_time, configs['development'].STRFTIME_FORMAT)
        if current < expire:
            return True
        else:
            return False
    return False


def get_user_info(session_id):
    """
    :function: 通过session_id 获取用户信息
    :param session_id:
    :return:
    """
    user = User.query.get_or_404(session_id)
    user_info = UserInfo.query.get_or_404(user.user_id)
    return user_info


def generate_token():
    """
    :function: 加密密token 用户信息+奖品信息+application_secret sha1算法
    :param:
    :return:
    """
    return None


def token_handler(award_token):
    """
    :function: 解密token
    :param award_token:
    :return:
    """
    return None


@app.route('/test')
def index():
    """
    :function: 测试页面
    :return: 测试页面
    """
    return render_template('test.html')


@app.route('/user/login', methods=['POST'])
def user_login():
    """
    :function: 微信小程序登陆
    :return: 返回state, msg, session_id. state 1表示成功，0表示异常，msg是错误信息，如果登陆成功，还会返回session_id
    """
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
    session_id = get_sha1(session_key.encode())
    current_time = datetime.datetime.utcnow()
    login_time = current_time.strftime(configs['development'].STRFTIME_FORMAT)
    session_id_expire_time = (current_time + datetime.timedelta(minutes=30)).strftime(
        configs['development'].STRFTIME_FORMAT)

    user = User.query.get_or_404(union_id)
    if user:
        user.login_time = login_time
        user.session_id_expire_time = session_id_expire_time
        user.session_key = session_key
        user.session_id = session_id
    else:
        user = User(open_id=open_id, union_id=union_id, session_key=session_key,
                    session_id=session_id, session_key_expire_time=session_id_expire_time)
    db.session.add(user)
    db.session.commit()
    res.update({
        'state': 1,
        'msg': '',
        'data': session_id
    })
    return jsonify(res)


@app.route('/user/info', methods=['POST'])
def user_info():
    """
    :function: 上传用户信息，最关键的是 nickName, avatarUrl 排行榜会用到
    :return:
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)


@app.route('/composition/upload', methods=['POST'])
def composition_upload():
    """
    :function: 上传图片 session_id
    :return:
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)
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
    user_info = get_user_info(session_id)
    filename = str(int(time.mktime(time.gmtime()))) + '_' + user_info.nickName + '.' + img.filename.split('.')[-1]
    image = dict()
    image.update({
        'name': filename,
        'date': datetime.datetime.utcnow().strftime(configs['development'].STRFTIME_FORMAT)
    })
    file_path = configs['development'].UPLOAD_FOLDER + image['name']
    image.update({'composition_url': configs['development'].COMPOSITION_PREFIX + image['name']})
    try:
        img.save(file_path)
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


@app.route('/rankinglist', methods=['POST'])
def get_rankinglist():
    """
    :function: 获取排行榜，分为婴儿车用户榜和非婴儿车用户榜，session_id, ranking_list_type
    :return: 根据用户类型，返回不同的排行榜，该榜单是即时生成的
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)


@app.route('/follow', methods=['POST'])
def follow():
    """
    :function: 帮玩家助力
    :return:
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)


@app.route('/raffle', methods=['POST'])
def raffle():
    """
    :function: 抽奖接口 session_id
    :return: 抽奖信息
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)


@app.route('/user/award/list', methods=['POST'])
def user_award_list():
    """
    :function: 获取我的奖品列表 session_id
    :return:
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)


@app.route('/user/award', methods=['POST'])
def user_award():
    """
    :function: 获取奖品以及收货信息 session_id
    :return:
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)


@app.route('/user/coupon', methods=['POST'])
def user_coupon():
    """
    :function: 用户的代金券信息 session_id
    :return:
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)


@app.route('/receive/award/<string:award_token>', methods=['GET'])
def user_coupon(award_token):
    """
    :function: 领奖专用链接 session_id
    :return:
    """
    token_handler(award_token)
    return render_template('')


