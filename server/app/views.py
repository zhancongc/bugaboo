import time
import json
import datetime
from app import app, db
from flask import jsonify, request, render_template
from .package import wxlogin, get_sha1
from .models import User, UserInfo, Composition, Follow, AwardRecord, Award, Express, Store
from config import configs
from functools import wraps


def logging(msg):
    with open('log.txt', 'a') as fp:
        fp.write(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + msg + '\n')
    print(msg)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in configs['development'].PICTURE_ALLOWED_EXTENSIONS


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


def login_required(func):
    """
    :function: 判断session_id是否有效
    :param func: 路由处理函数
    :return: 如果session_id验证通过，那么返回user对象
    """
    @wraps(func)
    def authenticate(*args, **kwargs):
        res = dict()
        session_id = request.headers.get('Session-Id')
        if not session_id:
            res.update({
                'state': 0,
                'msg': 'none session_id'
            })
            return jsonify(res)
        user = User.query.filter_by(session_id=session_id).first()
        if not user:
            res.update({
                'state': 0,
                'msg': 'cannot found session_id'
            })
            return jsonify(res)
        current = datetime.datetime.utcnow()
        expire = datetime.datetime.strptime(user.session_id_expire_time, configs['development'].STRFTIME_FORMAT)
        if current > expire:
            res.update({
                'state': 0,
                'msg': 'session_id expired'
            })
        return func(user, *args, **kwargs)
    return authenticate


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
        logging(json.dumps(res))
        return jsonify(res)
    try:
        wx = wxlogin(code)
    except Exception:
        res.update({
            'state': 0,
            'msg': 'weixin login error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    open_id = wx.get('openid')
    union_id = wx.get('unionid')
    session_key = wx.get('session_key')
    if open_id is None or union_id is None or session_key is None:
        res.update({
            'state': 0,
            'msg': 'open_id, union_id, session_key non existed'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 计算session_id
    session_id = get_sha1(session_key)
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
                        session_id=session_id, session_id_expire_time=session_id_expire_time)
            db.session.add(user)
        db.session.commit()
    except Exception:
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success',
        'data': session_id
    })
    logging(json.dumps(res))
    return jsonify(res)


@app.route('/user/info/upload', methods=['POST'])
@login_required
def user_info_upload(temp_user):
    """
    :function: 上传用户信息，最关键的是 nickName, avatarUrl 排行榜会用到
        avatarUrl, city, country, gender, language, nickName, province
    :return:
    """
    res = dict()
    avatarUrl = request.values.get('avatarUrl')
    city = request.values.get('city')
    country = request.values.get('country')
    gender = request.values.get('gender')
    language = request.values.get('language')
    nickName = request.values.get('nickName')
    province = request.values.get('province')
    if avatarUrl is None or city is None or country is None or gender is None or language is None or nickName is None or province is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 将用户信息写入数据库
    user_info_list = UserInfo.query.filter_by(user_id=temp_user.user_id).all()
    try:
        if len(user_info_list) == 0:
            user_info = UserInfo(user_id=temp_user.user_id, avatarUrl=avatarUrl, city=city, country=country,
                                 gender=gender, language=language, nickName=nickName, province=province)
        elif len(user_info_list) == 1:
            user_info= user_info_list[0]
            user_info.avatarUrl = avatarUrl
            user_info.city = city
            user_info.country = country
            user_info.gender = gender
            user_info.language = language
            user_info.nickName = nickName
            user_info.province = province
        else:
            res.update({
                'state': 0,
                'msg': 'save data to database error'
            })
            return jsonify(res)
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
@login_required
def user_composition_upload(temp_user):
    """
    :function: 上传作品 composition_type, composition
    :return:
    """
    res = dict()
    # 检查作品类型
    composition_type = request.values.get('composition_type')
    composition_angle = request.values.get('composition_angle')
    if composition_type is None or composition_angle is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 验证上传的图片
    img = request.files.get('composition')
    if img is None:
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
    user_info = UserInfo.query.filter_by(user_id=temp_user.user_id).first()
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
    composition_url = configs['development'].COMPOSITION_PREFIX + filename
    # 保存到数据库
    try:
        composition = Composition(user_id=temp_user.user_id, composition_type=composition_type,
                                  composition_angle=composition_angle, composition_name=filename,
                                  composition_url=composition_url)
        db.session.add(composition)
        db.session.commit()
    except Exception:
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        return jsonify(res)
    # 返回图片信息
    image = dict()
    composition = Composition.query.filter_by(user_id=temp_user.user_id).first()
    image.update({
        'composition_id': composition.composition_id,
        'composition_name': composition.composition_name,
        'composition_url': composition.composition_url,
        'composition_angle': composition.composition_angle,
        'composition_type': composition.composition_type,
        'timestamp': composition.timestamp
    })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': image
    })
    return jsonify(res)


@app.route('/user/composition', methods=['POST'])
@login_required
def user_composition(temp_user):
    """
    :function: 获取用户的作品信息 composition_id
    :return:
    """
    res = dict()
    composition_id = request.values.get('composition_id')
    if not composition_id:
        res.update({
            'state': 0,
            'msg': 'none composition id'
        })
        return jsonify
    # 获取作品信息
    temp_composition = Composition.query.filter_by(composition_id=composition_id).first()
    if temp_composition.user_id != temp_user.user_id:
        res.update({
            'state': 0,
            'msg': 'this is not your composition'
        })
        return jsonify(res)
    data = dict()
    data.update({
        'composition_id': temp_composition.composition_id,
        'composition_type': temp_composition.composition_type,
        'composition_angle': temp_composition.composition_angle,
        'composition_name': temp_composition.composition_name,
        'composition_url': temp_composition.composition_url
    })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/rankinglist', methods=['POST'])
@login_required
def rankinglist(temp_user):
    """
    :function: 获取排行榜，分为婴儿车用户榜和非婴儿车用户榜，session_id, ranking_list_type
    :return: 根据用户类型，返回不同的排行榜，该榜单是即时生成的
    """
    res = dict()
    temp_user
    res.update({
        'state': 1,
        'msg': 'success'
    })
    return jsonify(res)


@app.route('/user/follow', methods=['POST'])
@login_required
def user_follow(temp_user):
    """
    :function: 帮人助力，author_id
    :return: 助力成功
    """
    res = dict()
    # 助力
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


@app.route('/raffle', methods=['GET'])
@login_required
def raffle(temp_user):
    """
    :function: 抽奖接口
    :return: 抽奖信息
    """
    res = dict()
    # 抽奖逻辑
    pass
    award_id = 1
    try:
        # 发奖
        awardrecord = AwardRecord(award_id=award_id, user_id=temp_user.user_id)
        db.session.add(awardrecord)
        db.session.commit()
    except Exception:
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        return jsonify(res)
    award = Award.query.filter_by(award_id=award_id).first()
    data = dict()
    data.update({
        'award_id': award.award_id,
        'award_name': award.award_name,
        'award_image': award.award_image,
        'award_type': award.award_type,
        'award_description': award.award_description
    })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/user/award/list', methods=['GET'])
@login_required
def user_award_list(temp_user):
    """
    :function: 获取我的奖品列表
    :return: 返回所有奖品
    """
    res = dict()
    # 获取所有奖励
    temp_award_record_list = AwardRecord.query.filter_by(user_id=temp_user.user_id).all()
    if not temp_award_record_list:
        res.update({
            'state': 0,
            'msg': 'none award'
        })
        return jsonify(res)
    # 把所有奖励写入数组
    data = list()
    for temp in temp_award_record_list:
        awardrecord = dict()
        awardrecord.update({
            'award_record_id': temp.awardrecord_id,
            'award_id': temp.award_id,
            'user_id': temp.user_id,
            'checked': temp.checked,
            'check_time': temp.check_time,
            'detail_id': temp.detail_id,
            'awardrecord_type': temp.award_record_type
        })
        award = Award.query.filter_by(award_id=temp.award_id).first()
        awardrecord.update({
            'award_type': award.award_type,
            'award_name': award.award_name,
            'award_image': award.award_image,
            'award_description': award.award_description,
            'award_url': award.award_url
        })
        data.append(awardrecord)
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/user/award', methods=['POST'])
@login_required
def user_award(temp_user):
    """
    :function: 获取奖品以及收货信息 awardrecord_id
    :return:
    """
    res = dict()
    # 获取特定奖励
    awardrecord_id = request.values.get('awardrecord_id')
    if not awardrecord_id:
        res.update({
            'state': 0,
            'msg': 'none award record'
        })
        return jsonify(res)
    awardrecord = AwardRecord.query.filter_by(awardrecord_id=awardrecord_id).first()
    if not awardrecord:
        res.update({
            'state': 0,
            'msg': 'none award'
        })
        return jsonify(res)
    if awardrecord.user_id != temp_user.user_id:
        res.update({
            'state': 0,
            'msg': 'this is not your award'
        })
        return jsonify(res)
    # 把所有奖励写入数组
    data = dict()
    data.update({
        'award_record_id': awardrecord.awardrecord_id,
        'award_id': awardrecord.award_id,
        'user_id': awardrecord.user_id,
        'receiver': awardrecord.receiver,
        'phone': awardrecord.phone,
        'checked': awardrecord.checked,
        'check_time': awardrecord.check_time,
        'detail_id': awardrecord.detail_id,
        'awardrecord_type': awardrecord.award_record_type
    })
    award = Award.query.filter_by(award_id=awardrecord.award_id).first()
    data.update({
        'award_type': award.award_type,
        'award_name': award.award_name,
        'award_image': award.award_image,
        'award_description': award.award_description,
        'award_url': award.award_url
    })
    if awardrecord.awardrecord_type == 1:
        express = Express.query.filter_by(express_id=awardrecord.detail_id).first()
        if express:
            data.update({
                'express_id': express.express_id,
                'address': express.address,
                'is_dispatched': express.is_dispatched,
                'dispatch_bill': express.dispatch_bill,
                'dispatch_time': express.dispatch_time
            })
    elif awardrecord.awardrecord_id == 2:
        store = Store.query.filter_by(store_id=awardrecord.detail_id).first()
        if store:
            data.update({
                'store_id': store.store_id,
                'store_name': store.store_name,
                'store_city': store.store_city,
                'store_address': store.store_address
            })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/user/award/express', methods=['POST'])
@login_required
def user_award_express(temp_user):
    """
    :function: 上传奖品以及收货信息 awardrecord_id, express_type, receiver, phone, address, store_id
    :return:
    """
    res = dict()
    awardrecord_id = request.values.get('awardrecord_id')
    awardrecord_type = request.values.get('express_type')
    receiver = request.values.get('receiver')
    phone = request.values.get('phone')
    if awardrecord_type and receiver and phone:
        if awardrecord_type == 1:
            address = request.values.get('address')
        elif awardrecord_type == 2:
            store_id = request.values.get('store_id')
        elif awardrecord_id == 3:
            pass
        else:
            res.update({
                'state': 0,
                'msg': 'wrong awardrecord id'
            })
            return jsonify(res)
    else:
        res.update({
            'state': 0,
            'msg': 'lack for necessary data'
        })
        return jsonify(res)

    try:
        # 补全奖品记录
        awardrecord = AwardRecord.query.filter_by(awardrecord_id=awardrecord_id).first()
        if awardrecord.user_id != temp_user.user_id:
            res.update({
                'state': 0,
                'msg': 'award and user does not match'
            })
            return jsonify(res)
        awardrecord.awardrecord_type, awardrecord.receiver, awardrecord.phone = awardrecord_type, receiver, phone
        if awardrecord_type == 1:
            # 添加收货信息
            express = Express(awardrecord_id=awardrecord.awardrecord_id, address=address)
            awardrecord.detail_id = express.express_id
            db.session.add(express)
        if awardrecord_type == 2:
            # 关联门店信息
            awardrecord.detail_id = Store.query.filter_by(store_id=store_id).first()
        db.session.add(awardrecord)
        db.session.commit()
    except Exception:
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success'
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


