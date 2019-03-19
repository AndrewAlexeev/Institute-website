from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))
followers = db.Table('followers',
		db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
		db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
	)
class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	gender = db.Column(db.String(64), index=True, unique=False)
	news = db.relationship('New', backref='author', lazy='dynamic')
	avatar = db.Column(db.String(120),index=True,unique=False)
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	def __repr__(self):
		return '<User {}>'.format(self.name)
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(
			followers.c.followed_id == user.id).count() > 0
	def followed_posts(self):
		return New.query.join(
			followers, (followers.c.followed_id == New.user_id)).filter(
				followers.c.follower_id == self.id).order_by(
					New.timestamp.desc())


class New(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<New {}>'.format(self.body)
	