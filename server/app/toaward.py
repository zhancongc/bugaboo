import time
import hashlib
import configparser
from config import configs
import qrcode
from app import db
from app.models import Rank, AwardRecord, Award


conf = configparser.ConfigParser()
conf.read('config.ini')
app_secret = 'f103615743faddbf70bf8c90132fc9a6'


def to_award(temp_user, award):
    sh = hashlib.sha1()
    sh.update(str(temp_user.rank_user_id).encode())
    sh.update(str(award.award_id).encode())
    sh.update(app_secret.encode())
    sh.update(str(int(time.time())).encode())
    awardrecord_token = sh.hexdigest()
    qrcode_url = configs['development'].DOMAIN + configs['development'].QRCODE_URL_PREFIX + awardrecord_token
    # 保存图片到本地
    qrcode_name = str(int(time.mktime(time.gmtime()))) + '_' + awardrecord_token + '.png'
    qrcode_image_path = configs['development'].QRCODE_FOLDER
    image = qrcode.make(data=qrcode_url)
    image.save(qrcode_image_path + qrcode_name)
    qrcode_image_url = configs['development'].DOMAIN + '/static/qrcode/' + qrcode_name
    try:
        # 发奖
        awardrecord = AwardRecord(award_id=award.award_id, user_id=temp_user.rank_user_id,
                                  awardrecord_type=award.award_type,
                                  awardrecord_token=awardrecord_token, qrcode_image_url=qrcode_image_url)
        if award.award_id in [2, 4]:
            awardrecord.informed = True
        award.award_number -= 1
        db.session.add(temp_user)
        db.session.add(awardrecord)
        db.session.add(award)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

target = Rank.query.filter_by(number=101).all()
award = Award.query.filter_by(award_id=11).first()
for temp_user in target:
    to_award(temp_user, award)

'''
# 非Bugaboo用户
target = Rank.query.filter_by(number=1).all()
award = Award.query.filter_by(award_id=6).first()
for temp_user in target:
    to_award(temp_user, award)

target = Rank.query.filter(Rank.number<=10, Rank.number>1).all()
award = Award.query.filter_by(award_id=7).first()
for temp_user in target:
    to_award(temp_user, award)

target = Rank.query.filter(Rank.number<=50, Rank.number>=11).all()
award = Award.query.filter_by(award_id=8).first()
for temp_user in target:
    to_award(temp_user, award)

# Bugaboo用户
target = Rank.query.filter_by(number=51).all()
award = Award.query.filter_by(award_id=9).first()
for temp_user in target:
    to_award(temp_user, award)

target = Rank.query.filter(Rank.number<=60, Rank.number>51).all()
award = Award.query.filter_by(award_id=10).first()
for temp_user in target:
    to_award(temp_user, award)

target = Rank.query.filter(Rank.number<=100, Rank.number>=61).all()
award = Award.query.filter_by(award_id=11).first()
for temp_user in target:
    to_award(temp_user, award)

'''
