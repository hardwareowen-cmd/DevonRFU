from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):  # [web:21][web:24]
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    adminLevel = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_by = db.Column(db.String(120), nullable=False)
    club = db.Column(db.String(120), nullable=False)

    def set_adminLevel(self, adminLevel):
        self.adminLevel = adminLevel
    def set_userpassword(self, password):
        self.password_hash = generate_password_hash(password)  # [web:29][web:36]
    def check_userpassword(self, password):
        return check_password_hash(self.password_hash, password)
    def set_username(self, name):
        self.name = name
    def set_usercreated_by(self, created_by):
        self.created_by = created_by
    def set_userclub(self, club):
        self.club = club

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    ageGroup = db.Column(db.String(120), nullable=False)
    league = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(120), nullable=False)

    def set_ClubAgeGroup(self, ageGroup):
        self.ageGroup = ageGroup
    def set_ClubLeague(self, league):
        self.league = league
    def set_ClubLogo(self, logo):
        self.logo = logo

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    ageGroup = db.Column(db.String(120), nullable=False)
    season_id = db.Column(db.Integer, nullable=False)
    achived = db.Column(db.Boolean, nullable=False, default=False)
    def set_LeagueAgeGroup(self, ageGroup):
        self.ageGroup = ageGroup
    def set_LeagueSeason(self, season):
        self.season = season

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
