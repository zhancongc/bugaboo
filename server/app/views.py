import time
import datetime
from app import app, db
from flask import jsonify, request, render_template
from .package import wxlogin, get_sha1
from .models import User, UserInfo, Composition, Follow
from config import configs


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in configs['development'].PICTURE_ALLOWED_EXTENSIONS


def check_session_id(session_id):
    """
    :function: 检查用户登录状态是否失效
    :param session_id: session_id
    :return:
    """
    user = User.query.filter_by(session_id=session_id).first()
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
    user = User.query.filter_by(session_id).first()
    user_info = UserInfo.query.filter_by(user.user_id).first()
    return user_info


def generate_token():
    """
    :function: 加密密token user_id+award_id+application_secret sha1算法
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
    # 微信登陆
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
            'msg': 'weixin login error'
        })
        return jsonify(res)
    open_id = wx.get('openid')
    union_id = wx.get('unionid')
    session_key = wx.get('session_key')
    if open_id is None or union_id is None or session_key is None:
        res.update({
            'state': 0,
            'msg': 'open_id, union_id, session_key non existed'
        })
        return jsonify(res)
    # 计算session_id
    session_id = get_sha1(session_key.encode())
    current_time = datetime.datetime.utcnow()
    login_time = current_time.strftime(configs['development'].STRFTIME_FORMAT)
    session_id_expire_time = (current_time + datetime.timedelta(minutes=30)).strftime(
        configs['development'].STRFTIME_FORMAT)
    # 更新session信息，如果找不到这个用户，那么创建一个新的用户再更新信息
    temp_user = User.query.filter_by(union_id=union_id).first()
    try:
        if temp_user:
            temp_user.login_time = login_time
            temp_user.session_id_expire_time = session_id_expire_time
            temp_user.session_key = session_key
            temp_user.session_id = session_id
            db.session.add(temp_user)
        else:
            user = User(open_id=open_id, union_id=union_id, session_key=session_key,
                        session_id=session_id, session_key_expire_time=session_id_expire_time)
            db.session.add(user)
            user_info = UserInfo(user_id=user.user_id)
            db.session.add(user_info)
        db.session.commit()
    except Exception:
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success',
        'data': session_id
    })
    return jsonify(res)


@app.route('/user/info/upload', methods=['POST'])
def user_info_upload():
    """
    :function: 上传用户信息，最关键的是 nickName, avatarUrl 排行榜会用到
    session_key, avatarUrl, city, country, gender, language, nickName, province
    :return:
    """
    # 验证session_id
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)
    # 将用户信息写入数据库
    try:
        temp_user = User.query.filter_by(session_id=session_id).first()
        user_info = UserInfo(user_id=temp_user.user_id, avatarUrl=request.values.get('avatarUrl'),
                             city=request.values.get('city'), country=request.values.get('country'),
                             gender=request.values.get('gender'), language=request.values.get('language'),
                             nickName=request.values.get('nickName'), province=request.values.get('province'))
        db.session.add(user_info)
        db.session.commit()
    except Exception:
        res.update({
            'state': 0,
            'msg': 'save data to database error'
        })
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success'
    })
    return jsonify(res)


@app.route('/user/composition/upload', methods=['POST'])
def user_composition_upload():
    """
    :function: 上传作品 session_id
    :return:
    """
    res = dict()
    # 验证session_id
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)
    temp_user = User.query.filter_by('session_id').first()
    composition_type = request.values.get('composition_type')
    if not composition_type:
        res.update({
            'state': 0,
            'msg': 'None composition type'
        })
        return jsonify(res)
    # 验证上传的图片
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
    # 保存图片到本地
    user_info = get_user_info(session_id)
    filename = str(int(time.mktime(time.gmtime()))) + '_' + user_info.nickName + '.' + img.filename.split('.')[-1]
    file_path = configs['development'].UPLOAD_FOLDER + filename
    try:
        img.save(file_path)
    except Exception as e:
        res.update({
            'state': 0,
            'msg': 'Error occurred while saving file'
        })
        print(e)
        return jsonify(res)
    # 返回图片信息
    image = dict()
    image.update({
        'name': filename,
        'date': datetime.datetime.utcnow().strftime(configs['development'].STRFTIME_FORMAT),
        'composition_url': configs['development'].COMPOSITION_PREFIX + filename
    })
    # 保存到数据库
    try:
        composition = Composition(user_id=temp_user.user_id, composition_type=composition_type,
                                  composition_angle=composition_type, composition_name=filename,
                                  composition_url=image['composition_url'])
        db.session.add(composition)
        db.session.commit()
    except Exception:
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success',
        'data': image
    })
    return jsonify(res)


@app.route('/user/composition', methods=['POST'])
def user_composition():
    """
    :function: 获取用户的作品信息
    :return:
    """
    res = dict()
    # 验证session_id
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)
    # 获取作品信息
    temp_user = User.query.filter_by('session_id').first()
    temp_composition = Composition.query.filter_by(temp_user.user_id).first()
    composition = dict()
    composition.update({
        'composition_id': temp_composition.composition_id,
        'composition_type': temp_composition.composition_type,
        'composition_angle': temp_composition.composition_angle,
        'composition_name': temp_composition.composition_name,
        'composition_url': temp_composition.composition_url
    })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': composition
    })
    return jsonify(res)


@app.route('/rankinglist', methods=['POST'])
def rankinglist():
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


@app.route('/user/follow', methods=['POST'])
def user_follow():
    """
    :function: 帮人助力，author_id, temp_user.user_id
    :return: 助力成功
    """
    res = dict()
    # 验证session_id
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)
    # 助力
    temp_user = User.query.filter_by(session_id=session_id).first()
    author_id = request.values.get('author_id')
    if author_id:
        follow = Follow(followed_id=temp_user.user_id, follower_id=author_id)
        db.session.add(follow)
        db.session.commit()
    else:
        res.update({
            'state': 0,
            'msg': 'None this author id'
        })
    res.update({
        'state': 1,
        'msg': 'success'
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
    :return: 返回所有奖品
    """
    res = dict()
    session_id = request.values.get('session_id')
    if not session_id or not check_session_id(session_id):
        res.update({
            'state': 0,
            'msg': 'cannot found session_id or session_id expired'
        })
        return jsonify(res)
    temp_user = User.query.filter_by(session_id=session_id).first()




@app.route('/user/award/upload', methods=['POST'])
def user_award_upload():
    """
    :function: 上传奖品以及收货信息 session_id
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


@app.route('/receive/award/<string:award_token>', methods=['GET'])
def user_coupon(award_token):
    """
    :function: 领奖专用链接 session_id, award_token解密为用户的user_id, award_id和application_secret
    :return: 返回领奖成功的页面
    """
    token_handler(award_token)
    return render_template('receive_award.html')


