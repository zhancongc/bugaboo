from datetime import datetime
from app import db


class Follow(db.Model):
    __tablename__ = "follow"
    # 关注者
    followed_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), primary_key=True)
    # 被关注者
    follower_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class Composition(db.Model):
    __tablename__ = "composition"
    composition_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    composition_type = db.Column(db.Boolean(), default=False)
    composition_angle = db.Column(db.Integer(), default=0)
    composition_name = db.Column(db.String(64))
    composition_url = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.title


class Award(db.Model):
    __tablename__ = "award"
    """
    静态表，奖品信息
        实物：笔记本（30）、保温杯（50）、背包（70）。
        天猫券：2000-200（50)，1000-100（100），500-50（200）
    """
    award_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    award_name = db.Column(db.String(128))
    award_image = db.Column(db.String(256))
    award_type = db.Column(db.Integer, default=1)
    award_description = db.Column(db.Text())

    def __repr__(self):
        return '<Post %r>' % self.name


class AwardRecord(db.Model):
    """
    动态表，领奖表：领奖记录id，奖品id，用户id，领奖人姓名，领奖人手机，是否领奖，领奖时间
    如果奖品是实物，走快递，awardrecord_type = 1还要收货地址，发货单，是否发货，发货时间； receiver表
    如果走的是线下取货，awardrecord_type = 2 需要门店城市，门店名称，门店详细地址；store表
    如果奖品是天猫优惠券，awardrecord_type = 3；
    """
    __tablename__ = "awardrecord"
    record_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    award_id = db.Column(db.Integer(), db.ForeignKey('award.award_id'))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.user_id"))
    receiver = db.Column(db.String(16))
    phone = db.Column(db.String(11))
    checked = db.Column(db.Boolean(), default=False)
    check_time = db.Column(db.DateTime, default=datetime.utcnow)
    awardrecord_type = db.Column(db.Integer())
    detail_id = db.Column(db.Integer)


class Receiver(db.Model):
    """
    动态表，收货人信息，receiver_id连接了detail_id
    """
    __tablename__ = 'receiver'
    receiver_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receiver_address = db.Column(db.String(64))
    is_dispatched = db.Column(db.Boolean, default=False)
    dispatch_bill = db.Column(db.String(18))
    dispatch_time = db.Column(db.DateTime, default=datetime.utcnow)


class Store(db.Model):
    """
    静态表，所有门店信息，门店名称，城市，详细地址, store_id连接了store_id
    """
    __tablename__ = "store"
    store_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(128))
    store_city = db.Column(db.String(32))
    store_address = db.Column(db.String(256))


class UserInfo(db.Model):
    """
    动态表，用户信息表，微信开放信息
    """
    __tablename__ = "userinfo"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    avatarUrl = db.Column(db.String(128))
    city = db.Column(db.String(32))
    country = db.Column(db.String(32))
    gender = db.Column(db.Boolean())
    language = db.Column(db.String(8))
    nickName = db.Column(db.String(32))
    province = db.Column(db.String(32))


class User(db.Model):
    """
    动态表，用户表，包含登录信息，助力信息，领奖信息，作品信息
    """
    __tablename__ = "user"
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(28), unique=True, index=True)
    union_id = db.Column(db.String(28), unique=True, index=True)
    session_key = db.Column(db.String(24))
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(40))
    session_id_expire_time = db.Column(db.DateTime)
    can_raffle = db.Column(db.Boolean(), default=False)
    # user关注的人
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic', cascade='all, delete-orphan')
    # 被user关注的人
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic', cascade='all, delete-orphan')
    awardrecord_user_id = db.relationship('AwardRecord', foreign_keys=[AwardRecord.user_id],
                                          backref=db.backref('sender', lazy='joined'),
                                          lazy='dynamic', cascade='all, delete-orphan')
    composition_user_id = db.relationship('Composition', foreign_keys=[Composition.user_id],
                                          backref=db.backref('owner', lazy='joined'),
                                          lazy='dynamic', cascade='all, delete-orphan')

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(foll_id=None, follower=self, followed=user)
            db.session.add(f)

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.user_id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.user_id).first() is not None

    def __repr__(self):
        return '<User %r>' % self.user_id



