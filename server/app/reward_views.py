import random
import html
import time
import json
import requests
import datetime
import configparser
import hashlib
from config import configs
from app import app, db
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from .forms import GodLoginForm, ExchangeAwardForm
from .models import Award, God, AwardRecord
from .common import get_access_token
from .package import get_sha1


@app.route('/receive/award/<string:awardrecord_token>', methods=['GET'])
def receive_award(awardrecord_token):
    """
    :function: 领奖专用链接 session_id, awardrecord_token解密为用户的user_id, award_id和application_secret
    :return: 返回领奖成功的页面
    """
    # deadline = 1549814400
    deadline = 1548814400
    time_up = time.mktime(datetime.datetime.now().timetuple()) > deadline
    awardrecord_token = html.escape(awardrecord_token)
    awardrecords = AwardRecord.query.filter_by(awardrecord_token=awardrecord_token).all()
    if not awardrecords:
        return render_template('none_award.html', form=ExchangeAwardForm)
    award = Award.query.filter_by(award_id=awardrecords[0].award_id).first()
    print(award, awardrecords)
    if award:
        return render_template('receive_award.html', award_name=award.award_name, award_image=award.award_image,
                               time_up=time_up, checked=awardrecords[0].checked, token=awardrecords[0].awardrecord_token,
                               form=ExchangeAwardForm(), award_num=len(awardrecords),
                               check_time=awardrecords[0].check_time)
    else:
        return render_template('none_award.html', form=ExchangeAwardForm)


@app.route('/acquire/award', methods=['POST'])
def acquire_award():
    """
    :functino: 兑奖
    :return:
    """
    form = ExchangeAwardForm()
    if form.validate_on_submit():
        awardrecord_token = form.awardrecord_token.data
        exchange_token = form.exchange_token.data
        print('exchange_token', exchange_token)
        if awardrecord_token and exchange_token:
            awardrecord = AwardRecord.query.filter_by(awardrecord_token=awardrecord_token).first()
            if awardrecord:
                is_checked = awardrecord.check(exchange_token)
                db.session.add(awardrecord)
                db.session.commit()
                if is_checked:
                    return render_template('exchange_result.html', is_exchange=True)
    return render_template('exchange_result.html', is_exchange=False)


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
        print("客服message: ", message)
        open_id = message.get('FromUserName')
        response_data = dict()
        if message['MsgType'] == 'event' and message['Event'] == 'user_enter_tempsession':
            response_data.update({
                "touser": open_id,
                "msgtype": "text",
                "text": {
                    "content": "回复1，关注bugaboo官方公众号之后，可以到小程序【bugaboo用心说爱你】中抽奖"
                }
            })
        elif message['MsgType'] == 'text' and message['Content'] == '1':

            media_id = conf.get('weixin', 'media_id')
            response_data.update({
                "touser": open_id,
                "msgtype": "image",
                "image": {"media_id": media_id}
            })
        else:
            open_id = message['FromUserName']
            response_data.update({
                "touser": open_id,
                "msgtype": "text",
                "text": {
                    "content": "回复1，关注bugaboo官方公众号之后，可以到小程序【bugaboo用心说爱你】中抽奖"
                }
            })
        print('打印返回消息')
        print(response_data)
        access_token = get_access_token()
        if access_token:
            response_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + access_token
            res = requests.post(url=response_url, data=json.dumps(response_data, ensure_ascii=False).encode())
            print(res.text)
            return ''
        else:
            return ''


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
            value = str(value)
            access_token = get_sha1(value)
            current_time = datetime.datetime.utcnow()
            login_time = current_time.strftime(configs['development'].STRFTIME_FORMAT)
            access_token_expire_time = (current_time + datetime.timedelta(minutes=30)).strftime(
                configs['development'].STRFTIME_FORMAT)
            god = God(access_token=access_token, login_time=login_time, ip_addr=ip_addr,
                      access_token_expire_time=access_token_expire_time)
            db.session.add(god)
            db.session.commit()
            login_user(god)
            return redirect(url_for('god_index'))
        else:
            flash(message='用户名或者密码错误', category='warning')
    return render_template("god_login.html", form=form)


@app.route('/logout')
@login_required
def god_logout():
    logout_user()
    flash(message='您已注销')
    return redirect(url_for('god_login'))


@app.route('/god/index', methods=['GET'])
@login_required
def god_index():
    """
    :function: 后台首页， 搜索用户信息， 查看排行榜， 活动开启和关闭
    :return:
    """
    return render_template("god_index.html")

