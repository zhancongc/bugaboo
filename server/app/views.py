"""
Project     : bugaboo
Filename    : views.py
Author      : zhancongc
Description : 路由处理
"""

import time
import json
import datetime
import requests
import hashlib
import random
import configparser
from PIL import Image
from config import configs
from functools import wraps
from app import app, db
from flask import jsonify, request, render_template, redirect, url_for
from .package import wxlogin, get_sha1
from .models import User, UserInfo, Composition, AwardRecord, Award, Store, God
from .forms import GodLoginForm


def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    app_secret = conf.get('app', 'app_secret')
    res = requests.get(url.format(configs['development'].APP_ID, app_secret))
    access_token = json.loads(res.text).get('access_token')
    print(access_token)
    return access_token if access_token else None


def logging(msg):
    with open('response_log.txt', 'a') as fp:
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
        if session_id is None:
            res.update({
                'state': 0,
                'msg': 'none session_id'
            })
            return jsonify(res)
        user = User.query.filter_by(session_id=session_id).first()
        if user is None:
            res.update({
                'state': 0,
                'msg': 'cannot found session_id'
            })
            return jsonify(res)
        current = datetime.datetime.utcnow()
        expire = user.session_id_expire_time
        if current > expire:
            res.update({
                'state': 0,
                'msg': 'session_id expired'
            })
        return func(user, *args, **kwargs)
    return authenticate


def login_required2(func):
    """
    :function: 判断后台是否登录
    :param func: 路由处理函数
    :return: 原样返回
    """
    @wraps(func)
    def whether_login(*args, **kwargs):
        ip_addr = request.remote_addr
        access_token = request.headers.get('Access-Token')
        if access_token is None:
            return redirect(url_for('god_login'))
        god = God.query.filter_by(access_token=access_token).first()
        if god is None:
            return redirect(url_for('god_login'))
        current = datetime.datetime.utcnow()
        expire = god.access_token_expire_time
        if current > expire:
            return redirect(url_for('god_login'))
        return func(*args, **kwargs)
    return whether_login


@app.route('/test')
def test():
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
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'weixin login error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    open_id = wx.get('openid')
    session_key = wx.get('session_key')
    if open_id is None or session_key is None:
        res.update({
            'state': 0,
            'msg': 'open_id, session_key non existed'
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
    temp_user = User.query.filter_by(open_id=open_id).first()
    try:
        if temp_user:
            temp_user.login_time = login_time
            temp_user.session_id_expire_time = session_id_expire_time
            temp_user.session_key = session_key
            temp_user.session_id = session_id
            db.session.add(temp_user)
        else:
            temp_user = User(open_id=open_id, session_key=session_key,
                        session_id=session_id, session_id_expire_time=session_id_expire_time)
            db.session.add(temp_user)
        db.session.commit()
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    data = {
        'session_id': session_id,
        'can_raffle': temp_user.can_raffle,
        'can_follow': temp_user.can_follow,
    }
    if temp_user:
        composition = Composition.query.filter_by(user_id=temp_user.user_id).first()
        if composition:
            data.update({
                'composition_id': composition.composition_id
            })
    else:
        res.update({
            'state': 2,
            'msg': 'new user',
            'data': data
        })
        logging(json.dumps(res))
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
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
    avatar_url = request.values.get('avatarUrl')
    city = request.values.get('city')
    country = request.values.get('country')
    gender = request.values.get('gender')
    language = request.values.get('language')
    nick_name = request.values.get('nickName')
    province = request.values.get('province')
    if avatar_url is None or city is None or country is None or gender is None or language is None \
            or nick_name is None or province is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        gender = int(gender)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: gender'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 将用户信息写入数据库
    user_info_list = UserInfo.query.filter_by(user_id=temp_user.user_id).all()
    try:
        if len(user_info_list) == 0:
            user_info = UserInfo(user_id=temp_user.user_id, avatarUrl=avatar_url, city=city, country=country,
                                 gender=gender, language=language, nickName=nick_name, province=province)
        elif len(user_info_list) == 1:
            user_info = user_info_list[0]
            user_info.avatarUrl = avatar_url
            user_info.city = city
            user_info.country = country
            user_info.gender = gender
            user_info.language = language
            user_info.nickName = nick_name
            user_info.province = province
        else:
            res.update({
                'state': 0,
                'msg': 'cannot upload user info'
            })
            return jsonify(res)
        db.session.add(user_info)
        db.session.commit()
    except Exception as e:
        print(e)
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


@app.route('/user/composition/info', methods=['GET'])
@login_required
def user_composition_info(temp_user):
    """
    :function: 判断是否有作品
    :return: composition_id, nickName, avatarUrl
    """
    res = dict()
    # 根据session_id 拉去user_info和composition_id
    temp_composition = Composition.query.filter_by(user_id=temp_user.user_id).first()
    if temp_composition is None:
        res.update({
            'state': 2,
            'msg': 'new user'
        })
        return jsonify(res)
    user_info = UserInfo.query.filter_by(user_id=temp_user.user_id).first()
    if user_info is None:
        res.update({
            'state': 0,
            'msg': 'cannot found user info'
        })
        return jsonify(res)
    data = dict()
    data.update({
        'user_id': user_info.user_id,
        'nickName': user_info.nickName,
        'avatarUrl': user_info.avatarUrl,
        'composition_id': temp_composition.composition_id
    })
    res.update({
        'state': 1,
        'msg': 'get user info and composition',
        'data': data
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
    # 检查用户是否有作品，有作品直接免谈
    temp_composition = Composition.query.filter_by(user_id=temp_user.user_id).first()
    if temp_composition:
        res.update({
            'state': 0,
            'msg': 'you have uploaded composition'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 检查作品类型
    composition_type = request.values.get('composition_type')
    composition_angle = request.values.get('composition_angle')
    if composition_type is None or composition_angle is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 类型转换
    try:
        composition_type = int(composition_type)
        composition_angle = int(composition_angle)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: composition angle or type'
        })
        logging(json.dumps(res))
        return jsonify(res)
    if composition_angle not in [0, 90, 180, 270]:
        res.update({
            'state': 0,
            'msg': 'value error: composition angle'
        })
        logging(json.dumps(res))
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
        logging(json.dumps(res))
        return jsonify(res)
    # 保存图片到本地
    filename = str(int(time.mktime(time.gmtime()))) + '_' + img.filename
    file_path = configs['development'].UPLOAD_FOLDER + filename
    try:
        img.save(file_path)
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'Error occurred while saving file'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 如果图片需要旋转
    if composition_angle in [90, 180, 270]:
        im = Image.open(file_path)
        if composition_angle == 90:
            out = im.transpose(Image.ROTATE_270)
            out.save(file_path)
        elif composition_angle == 180:
            out = im.transpose(Image.ROTATE_180)
            out.save(file_path)
        else:
            out = im.transpose(Image.ROTATE_90)
            out.save(file_path)
    # 图片压缩
    im = Image.open(file_path)
    im_a, im_b = im.size
    if im_a > im_b:
        im_long, im_short = im_a, im_b
        if im_short > 600:
            coef = 600 / im_short
            im_long_modify = int(im_long * coef)
            im_short_modify = 600
            im.resize((im_long_modify, im_short_modify))
        if im_long > 1200:
            coef = 1200 / im_long
            im_short_modify = int(im_short * coef)
            im_long_modify = 1200
            im.resize((im_long_modify, im_short_modify))
    else:
        im_long, im_short = im_b, im_a
        if im_short > 600:
            coef = 600/im_short
            im_long_modify = int(im_long*coef)
            im_short_modify = 600
            im.resize((im_short_modify, im_long_modify))
        if im_long > 1200:
            coef = 1200/im_long
            im_short_modify = int(im_short*coef)
            im_long_modify = 1200
            im.resize((im_short_modify, im_long_modify))
    im.save(file_path)
    # 图片处理完成，生成图片的URI
    composition_url = configs['development'].COMPOSITION_PREFIX + filename
    # 保存到数据库
    try:
        composition = Composition(user_id=temp_user.user_id, composition_type=composition_type,
                                  composition_name=filename, composition_url=composition_url)
        db.session.add(composition)
        composition.sync_user_type()
        db.session.commit()
        composition_id = composition.composition_id
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 返回图片信息
    image = dict()
    composition = Composition.query.filter_by(composition_id=composition_id).first()
    image.update({
        'composition_id': composition.composition_id,
        'composition_name': composition.composition_name,
        'composition_url': composition.composition_url,
        'composition_type': composition.composition_type,
        'timestamp': composition.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': image
    })
    logging(json.dumps(res))
    return jsonify(res)


@app.route('/user/composition', methods=['POST'])
@login_required
def user_composition(temp_user):
    """
    :function: 根据composition_id查找作品信息 composition_id
    :return:
    """
    res = dict()
    composition_id = request.values.get('composition_id')
    if composition_id is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        composition_id = int(composition_id)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: composition id'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 获取作品信息
    composition = Composition.query.filter_by(composition_id=composition_id).first()
    if composition is None:
        res.update({
            'state': 0,
            'msg': 'none composition id'
        })
        return jsonify(res)
    user_info = UserInfo.query.filter_by(user_id=composition.user_id).first()
    if user_info is None:
        res.update({
            'state': 0,
            'msg': 'his or her user info is not intact'
        })
        return jsonify(res)
    data = dict()
    data.update({
        'user_id': temp_user.user_id,
        'nickName': user_info.nickName,
        'avatarUrl': user_info.avatarUrl,
        'composition_id': composition.composition_id,
        'composition_type': composition.composition_type,
        'composition_name': composition.composition_name,
        'composition_url': composition.composition_url,
        'timestamp': composition.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })
    if composition.user_id != temp_user.user_id:
        '''
        user = User.query.filter_by(user_id=composition.user_id).first()
        followers = list()
        followers.append()
        data.update({
            'follow_times': user.follow_times,
            'followers': followers
        })
        '''
        res.update({
            'state': 2,
            'msg': 'others composition',
            'data': data
        })
    else:
        res.update({
            'state': 1,
            'msg': 'my composition',
            'data': data
        })
    return jsonify(res)


@app.route('/rankinglist', methods=['POST'])
@login_required
def rankinglist(temp_user):
    """
    :function: 获取排行榜，分为婴儿车用户榜和非婴儿车用户榜, ranking_list_type
    :return: 根据用户类型，返回不同的排行榜，该榜单是即时生成的
    """
    print(temp_user)
    res = dict()
    ranking_list_type = request.values.get('ranking_list_type')
    if ranking_list_type is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        ranking_list_type = int(ranking_list_type)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: ranking list type'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 获取排行榜用户信息
    data = list()
    if ranking_list_type in [0, 1]:
        user_list = User.query.filter_by(user_type=ranking_list_type).order_by(User.follow_times).limit(50).desc()
        for index in range(len(user_list)):
            user_info = UserInfo.query.filter_by(user_id=user_list['index'].user_id).first()
            temp = {
                'index': index,
                'nickName': user_info.nickName,
                'avatarUrl': user_info.avatarUrl,
                'follow_times': user_list['index'].follow_times
            }
            list.append(temp)
    else:
        res.update({
            'state': 0,
            'msg': 'invalid ranking list type'
        })
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success',
        'ranking_list_type': ranking_list_type,
        'data': data
    })
    return jsonify(res)


@app.route('/user/follow', methods=['POST'])
@login_required
def user_follow(temp_user):
    """
    :function: 帮人助力，composition_id
    :return: 助力成功
    """
    res = dict()
    # 助力
    composition_id = request.values.get('composition_id')
    if composition_id is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        composition_id = int(composition_id)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: ranking list type'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 找到作品对应的用户
    composition = Composition.query.filter_by(composition_id=composition_id).first()
    if composition is None:
        res.update({
            'state': 0,
            'msg': 'invalid composition_id'
        })
        logging(json.dumps(res))
        return jsonify(res)
    author_id = composition.user_id
    # 助力的用户必须存在还不能是自己
    user = User.query.filter_by(user_id=author_id).first()
    if user is None:
        res.update({
            'state': 0,
            'msg': 'cannot find owner'
        })
        return jsonify(res)
    if temp_user.user_id == user.user_id:
        res.update({
            'state': 2,
            'msg': 'not myself'
        })
        return jsonify(res)
    # 尝试助力，把数据写入数据库
    try:
        temp_user.follow(user)
        db.session.commit()
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'write to db error'
        })
        return jsonify(res)
    data = {
        'followed_id': temp_user.user_id,
        'follower_id': user.user_id
    }
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
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
    except Exception as e:
        print(e)
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
    if temp_award_record_list is None:
        res.update({
            'state': 2,
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
            'awardrecord_token': temp.award_record_token,
            'checked': temp.checked,
            'check_time': temp.check_time.strftime('%Y-%m-%d %H:%M:%S'),
            'store_id': temp.store_id,
            'awardrecord_type': temp.award_record_type
        })
        award = Award.query.filter_by(award_id=temp.award_id).first()
        awardrecord.update({
            'award_type': award.award_type,
            'award_name': award.award_name,
            'award_image': award.award_image,
            'award_description': award.award_description
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
    if awardrecord_id is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        awardrecord_id = int(awardrecord_id)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: award record id'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 查找这条奖品记录
    awardrecord = AwardRecord.query.filter_by(awardrecord_id=awardrecord_id).first()
    if awardrecord is None:
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
        'check_time': awardrecord.check_time.strftime('%Y-%m-%d %H:%M:%S'),
        'store_id': awardrecord.store_id,
        'awardrecord_type': awardrecord.award_record_type,
        'awardrecord_token': awardrecord.awardrecord_token
    })
    award = Award.query.filter_by(award_id=awardrecord.award_id).first()
    data.update({
        'award_type': award.award_type,
        'award_name': award.award_name,
        'award_image': award.award_image,
        'award_description': award.award_description
    })
    if awardrecord.awardrecord_id == 2:
        store = Store.query.filter_by(store_id=awardrecord.store_id).first()
        if store:
            data.update({
                'store_id': store.store_id,
                'store_name': store.store_name,
                'store_city': store.store_city,
                'store_address': store.store_address,
                'store_phone': store.store_phone
            })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/user/award/store', methods=['POST'])
@login_required
def user_award_express(temp_user):
    """
    :function: 上传奖品以及门店信息 awardrecord_id, receiver, phone, store_id
    :return:
    """
    res = dict()
    awardrecord_id = request.values.get('awardrecord_id')
    receiver = request.values.get('receiver')
    phone = request.values.get('phone')
    store_id = request.values.get('store_id')
    # 检查空值
    if awardrecord_id is None or receiver is None or phone is None or store_id is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        awardrecord_id = int(awardrecord_id)
        store_id = int(store_id)
        receiver = int(receiver)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 检查奖品和用户是否对应
    awardrecord = AwardRecord.query.filter_by(awardrecord_id=awardrecord_id).first()
    if awardrecord.user_id != temp_user.user_id:
        res.update({
            'state': 0,
            'msg': 'award and user does not match'
        })
        return jsonify(res)
    # 检查门店是否存在
    store_id = Store.query.filter_by(store_id=store_id).first()
    if store_id is None:
        res.update({
            'state': 0,
            'msg': 'invalid store'
        })
        return jsonify(res)
    # 添加收货记录
    try:
        awardrecord.receiver, awardrecord.phone, awardrecord.store_id = receiver, phone, store_id
        db.session.add(awardrecord)
        db.session.commit()
    except Exception as e:
        print(e)
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


@app.route('/online/service', methods=['GET', 'POST'])
def online_service():
    signature = request.values.get("signature")
    timestamp = request.values.get("timestamp")
    nonce = request.values.get("nonce")
    print('signature, timestamp, nonce', signature, timestamp, nonce)
    if signature is None or timestamp is None or nonce is None:
        return 'bad guys'
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    token = conf.get('app', 'online_service_token')
    params = list()
    params.append(token)
    params.append(timestamp)
    params.append(nonce)
    params.sort()
    out = ''
    for i in params:
        out += i
    sign = hashlib.sha1(out.encode()).hexdigest()
    if sign != signature:
        return 'bad guys'
    if request.method == 'GET':
        echostr = request.values.get("echostr")
        if echostr:
            return echostr
        else:
            return 'bad guys'
    if request.method == 'POST':
        message = json.loads(request.get_data(as_text=True))
        print("message", message)
        open_id = message['FromUserName']
        response_data = dict()
        if message['MsgType'] == 'text' and message['Content'] == '1':
            media_id = conf.get('weixin', 'media_id')
            response_data.update({
                "touser": open_id,
                "msgtype": "image",
                "image": {"media_id": media_id}
            })
        else:
            response_data.update({
                "touser": open_id,
                "msgtype": "text",
                "text": {
                    "content": "回复1，关注bugaboo官方公众号之后，可以到小程序【bugaboo助力】中抽奖"
                }
            })
        print('打印返回消息')
        print(response_data)
        access_token = get_access_token()
        if access_token:
            response_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + access_token
            res = requests.post(url=response_url, data=json.dumps(response_data, ensure_ascii=False))
            print(res.text)
            return 'good luck'
        else:
            return 'bad news'


@app.route('/god/login', methods=['GET', 'POST'])
def god_login():
    """
    :function: 管理员登陆
    :return:
    """
    form = GodLoginForm()
    if form.validate_on_submit():
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        if conf.get('weixin', 'god_name') == form.username.data and \
                        conf.get('weixin', 'god_password') == form.password.data:
            ip_addr = request.remote_addr
            value = random.random()
            value = hash(value)
            value = str(value).encode()
            access_token = get_sha1(value)
            current_time = datetime.datetime.utcnow()
            login_time = current_time.strftime(configs['development'].STRFTIME_FORMAT)
            access_token_expire_time = (current_time + datetime.timedelta(minutes=30)).strftime(
                configs['development'].STRFTIME_FORMAT)
            god = God(access_token=access_token, login_time=login_time, ip_addr=ip_addr,
                      access_token_expire_time=access_token_expire_time)
            db.session.add(god)
            db.session.commit()
            return redirect(url_for('god_index'))
    return render_template("god_login.html", form=form)


@app.route('/god/index', methods=['GET'])
@login_required2
def god_index():
    """
    :function: 后台首页， 搜索用户信息， 查看排行榜， 活动开启和关闭
    :return:
    """
    return render_template("god_index.html")




