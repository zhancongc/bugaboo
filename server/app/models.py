from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = "User"
    # oy08L0Zmm6pSjsfj6H0K9hbTC0zM
    user_id = db.Column(db.Integer(), primary_key=True)
    open_id = db.Column(db.String(28), unique=True, index=True)
    avatarUrl = db.Column(db.String(128))
    city = db.Column(db.String(32))
    country = db.Column(db.String(32))
    gender = db.Column(db.Boolean())
    language = db.Column(db.String(8))
    nickName = db.Column(db.String(32))
    province = db.Column(db.String(32))
    login_time = db.Column(db.Date, default=datetime.utcnow)
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
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


class Follow(db.Model):
    __tablename__ = "Follow"
    foll_id = db.Column(db.Integer(), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    timestamp = db.Column(db.Date, default=datetime.utcnow)


class Photograph(db.Model):
    __tablename__ = "Photograph"
    photograph_id = db.Column(db.Integer(), primary_key=True)
    owner = db.Column(db.Integer(), db.Foreign_key('User.user_id'))
    title = db.Column(db.String(64))
    path = db.Column(db.String())

    def __repr__(self):
        return '<Post %r>' % self.title


class Award(db.Model):
    __tablename__ = "Award"
    award_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())

    def __repr__(self):
        return '<Post %r>' % self.name


class AwardRecord(db.Model):
    __tablename__ = "AwardRecord"
    record_id = db.Column(db.Integer(), primary_key=True)
    award_id = db.Column(db.Integer(), db.ForeignKey('Award.award_id'))
    receiver = db.Column(db.String(64))
    phone = db.Column(db.String(11))
    checked = db.Column(db.Boolean(), default=False)


class RankingList(db.Model):
    __tablename__ = "RankingList"
    user = db.Column(db.String(), db.ForeignKey('User.user_id'))
    followers = db.Column(db.String(), db.ForeignKey('User.openid'))





