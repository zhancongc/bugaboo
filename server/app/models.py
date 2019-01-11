from datetime import datetime
from app import db
from app import login_manager

class Follow(db.Model):
    __tablename__ = "follow"
    follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 关注者
    followed_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    # 被关注者
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Composition(db.Model):
    __tablename__ = "composition"
    composition_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), index=True, nullable=False)
    composition_type = db.Column(db.Integer, default=0, nullable=False)
    composition_msg = db.Column(db.String(256))
    composition_url = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def sync_user_type(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        if user is None:
            return False
        user.user_type = self.composition_type
        db.session.add(user)
        return True

    def __repr__(self):
        return '<Post %r>' % self.title


class Award(db.Model):
    __tablename__ = "award"
    """
    静态表，奖品信息 award_type: 默认为1（实物)，优惠券是2
        实物：笔记本（30）、保温杯（50）、背包（70）。
        天猫券：2000-200（50)，1000-100（100），500-50（200）
    """
    award_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    award_name = db.Column(db.String(128), nullable=False)
    award_image = db.Column(db.String(256))
    award_type = db.Column(db.Integer, default=1)
    award_description = db.Column(db.Text())
    award_number = db.Column(db.Integer, nullable=False)
    exchange_token = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.name


class AwardRecord(db.Model):
    """
    动态表，领奖表：领奖记录id，奖品id，用户id，领奖人姓名，领奖人手机，是否领奖，领奖时间
    如果走的是线下取货，awardrecord_type = 1 需要门店城市，门店名称，门店详细地址；store表
    如果奖品是天猫优惠券，awardrecord_type = 2；
    如果是快递，awardrecord_type = 2，需要详细地址
    """
    __tablename__ = "awardrecord"
    awardrecord_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    award_id = db.Column(db.Integer, db.ForeignKey('award.award_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    awardrecord_type = db.Column(db.Integer, nullable=False)
    store_id = db.Column(db.Integer)
    receiver = db.Column(db.String(16))
    phone = db.Column(db.String(11))
    address = db.Column(db.String(256))
    checked = db.Column(db.Boolean, default=False)
    check_time = db.Column(db.DateTime, default=datetime.utcnow)
    awardrecord_token = db.Column(db.String(128), nullable=False)
    qrcode_image_url = db.Column(db.String(128), nullable=False)

    def check(self):
        self.checked = True
        self.check_time = datetime.utcnow()

    def set_address(self, address, receiver, phone):
        self.address = address
        self.receiver = receiver
        self.phone = phone

    def set_store(self, store_id, receiver, phone):
        self.store_id = store_id
        self.receiver = receiver
        self.phone = phone

class Store(db.Model):
    """
    静态表，所有门店信息，门店名称，城市，详细地址, 联系电话, store.store_id 连接了awardrecord.detail_id
    """
    __tablename__ = "store"
    store_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(128))
    store_city = db.Column(db.String(32))
    store_address = db.Column(db.String(256))
    store_phone = db.Column(db.String(32))


class UserInfo(db.Model):
    """
    动态表，用户信息表，微信开放信息
    """
    __tablename__ = "userinfo"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True, nullable=True)
    city = db.Column(db.String(32))
    country = db.Column(db.String(32))
    gender = db.Column(db.Integer)
    language = db.Column(db.String(8))
    province = db.Column(db.String(32))


class User(db.Model):
    """
    动态表，用户表，包含登录信息，助力信息，领奖信息，作品信息
    """
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(28), unique=True, index=True, nullable=False)
    session_key = db.Column(db.String(24), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(40), nullable=False)
    session_id_expire_time = db.Column(db.DateTime, nullable=False)
    can_raffle = db.Column(db.Boolean, default=False)
    can_follow = db.Column(db.Boolean, default=True)
    user_type = db.Column(db.Integer, default=0)
    follow_times = db.Column(db.Integer, default=0)
    nickName = db.Column(db.String(32))
    avatarUrl = db.Column(db.String(512))
    # user关注的人
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic', cascade='all, delete-orphan')
    # 关注user的人
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
            foll = Follow(follower=self, followed=user)
            self.follow_times += 1
            db.session.add(foll)
            db.session.add(self)
            self.can_follow = False

    def raffle(self):
        self.can_raffle = not self.can_raffle

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.user_id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.user_id).first() is not None

    def __repr__(self):
        return '<User %r>' % self.user_id


class God(db.Model):
    """
    后台登陆表，登陆成功后，记录用户的ip地址
    """
    god_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    access_token = db.Column(db.String(40), nullable=True)
    ip_addr = db.Column(db.String(15))
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    access_token_expire_time = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.god_id


@login_manager.user_loader
def load_user(god_id):
    return God.query.get(int(god_id))
