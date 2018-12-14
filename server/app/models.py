from datetime import datetime, timedelta
from app import db


class Follow(db.Model):
    __tablename__ = "follow"
    # 关注者
    followed_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), primary_key=True)
    # 被关注者
    follower_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), primary_key=True)
    follow_time = db.Column(db.DateTime(), default=datetime.utcnow)


class Photograph(db.Model):
    __tablename__ = "photograph"
    photograph_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    title = db.Column(db.String(64))
    description = db.Column(db.String(128))
    path = db.Column(db.String(128))

    def __repr__(self):
        return '<Post %r>' % self.title


class AwardRecord(db.Model):
    __tablename__ = "awardrecord"
    record_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    award_id = db.Column(db.Integer(), db.ForeignKey('award.award_id'))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.user_id"))
    receiver = db.Column(db.String(64))
    phone = db.Column(db.String(11))
    checked = db.Column(db.Boolean(), default=False)
    check_time = db.Column(db.DateTime, default=datetime.utcnow)


class UserInfo(db.Model):
    __tablename__ = "userinfo"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    avatarUrl = db.Column(db.String(128))
    city = db.Column(db.String(32))
    country = db.Column(db.String(32))
    gender = db.Column(db.Boolean())
    language = db.Column(db.String(8))
    nickName = db.Column(db.String(32))
    province = db.Column(db.String(32))

class RankingList(db.Model):
    __tablename__ = "rankinglist"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    follow_number = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = "user"
    # oy08L0Zmm6pSjsfj6H0K9hbTC0zM
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(28), unique=True, index=True)
    union_id = db.Column(db.String(28), unique=True, index=True)
    session_key = db.Column(db.String(24))
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(40))
    session_id_expire_time = db.Column(db.DateTime)
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
    photograph_user_id = db.relationship('Photograph', foreign_keys=[Photograph.user_id],
                                         backref=db.backref('owner', lazy='joined'),
                                         lazy='dynamic', cascade='all, delete-orphan')
    rankinglist_user_id = db.relationship('RankingList', foreign_keys=[RankingList.user_id],
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
        return '<User %r>' % self.nickName


class Award(db.Model):
    __tablename__ = "award"
    award_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    award_name = db.Column(db.String(128))
    description = db.Column(db.Text())

    def __repr__(self):
        return '<Post %r>' % self.name


