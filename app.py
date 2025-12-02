# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import logout_user, current_user, login_required, login_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from Decorators import access_level_required

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"  # simple file DB [web:28]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "change-this-secret-key"

db = SQLAlchemy(app)
from models import User, Club, League, Season

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/boys')
def boys():
    return render_template("boys.html")

@app.route('/girls')
def girls():
    return render_template("girls.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember") is not None

        # Look up user in the database
        user = User.query.filter_by(email=email).first()

        # Check password against stored hash
        if user and user.check_userpassword(password):
            print("hello")
            # If using Flask-Login you would do:
            login_user(user, remember=remember)
            return redirect(url_for("admin_dashboard"))

        flash("Invalid email or password")

    # GET request or failed POST -> re-render login page
    return render_template("login.html")

@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    return render_template("adminDashboard.html")

@app.route('/admin-logout')
def admin_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/add-league-admin',methods=["GET", "POST"])
@access_level_required(2)
def add_league_admin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        if User.query.filter_by(email=email).first():
            flash({"text":"Email already registered"},category="alert alert-danger")
            return redirect(url_for("add_league_admin"))

        admin = User(email=email)
        admin.set_adminLevel(2)
        admin.set_userpassword(password)
        admin.set_username(name)
        admin.set_usercreated_by(current_user.name)
        admin.set_userclub("none")

        with app.app_context():
            db.session.add(admin)
            db.session.commit()
            flash({"text": "Account Created Successfully"}, category="alert alert-success")
            return redirect(url_for("add_league_admin"))
    return render_template("createLeagueAdmin.html")


@app.route('/add-club-admin',methods=["GET", "POST"])
@access_level_required(2)
def add_club_admin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        club = request.form.get("club")
        if User.query.filter_by(email=email).first():
            flash({"text": "Email already registered"}, category="alert alert-danger")
            return redirect(url_for("add_club_admin"))

        admin = User(email=email)
        admin.set_adminLevel(2)
        admin.set_password(password)
        admin.set_name(name)
        admin.set_created_by(current_user.name)
        admin.set_club(club)

        with app.app_context():
            db.session.add(admin)
            db.session.commit()
            flash({"text": "Account Created Successfully"}, category="alert alert-success")
            return redirect(url_for("add_club_admin"))
    return render_template("createClubAdmin.html")


@app.route('/add-club',methods=["GET", "POST"])
@access_level_required(2)
def add_club():
    seasons = []
    if request.method == "POST":
        name = request.form.get("name")
        leagueID = request.form.get("league")
        league = db.session.query(League).get(league_id)
        if league:
            age_group = league.ageGroup
            print(f"Age group for league {league_id}: {age_group}")
        logo = request.form.get("logo")
        if Club.query.filter_by(name=name, ageGroup=ageGroup).first():
            flash({"text":"Club already exists"}, category="alert alert-danger")
            return redirect(url_for("add_club"))

        club= Club(name=name)
        club.set_ClubAgeGroup(ageGroup)
        league_obj = db.session.query(League).filter_by(name=leagueID).first()
        club.set_ClubLeague(league_obj)
        club.set_ClubLogo(logo)

        with app.app_context():
            db.session.add(club)
            db.session.commit()
            flash({"text": "Club Created Successfully"}, category="alert alert-success")
            return redirect(url_for("add_club"))
    seasons = Season.query.all()
    logos = []
    for file in os.listdir('./static/Club_Logos'):
        logos.append(file)
    return render_template("createClub.html", seasons=seasons, logos=logos)

@app.route('/leagueinfofetch')
@access_level_required(2)
def leagueinfofetch():
    leagues = [{"id":x.id,"name": x.name, "season_id": x.season_id} for x in League.query.all()]
    leagues = jsonify(leagues)
    return(leagues)

@app.route('/add-league',methods=["GET", "POST"])
@access_level_required(2)
def add_league():
    if request.method == "POST":
        name = request.form.get("name")
        ageGroup = request.form.get("ageGroup")
        season = request.form.get("season")

        if not name:
            flash({"text": "No League name added"}, category="alert alert-danger")
            return redirect(url_for("add_league"))
        if League.query.filter_by(name=name).first():
            flash({"text": "League already exists"}, category="alert alert-danger")
            return redirect(url_for("add_league"))
        league = League(name=name, ageGroup=ageGroup, season_id=season)
        with app.app_context():
            db.session.add(league)
            db.session.commit()
            flash({"text": "League Created Successfully"}, category="alert alert-success")
            return redirect(url_for("add_league"))
    seasons = Season.query.all()
    return render_template("createLeague.html", seasons=seasons)


@app.route('/add-season',methods=["GET", "POST"])
@access_level_required(2)
def add_season():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            flash({"text": "Season name not inputed"}, category="alert alert-danger")
            return redirect(url_for("add_season"))

        if Season.query.filter_by(name=name).first():
            flash({ "text": "Season already exists"}, category="alert alert-danger")
            return redirect(url_for("add_season"))

        season = Season(name=name)
        with app.app_context():
            db.session.add(season)
            db.session.commit()
            flash({"text": "Season Created Successfully"}, category="alert alert-success")
            return redirect(url_for("add_season"))
    return render_template("createSeason.html")

@app.route('/add-Fixtures',methods=["GET", "POST"])
@access_level_required(2)
def add_fixtures():
    if request.method == "POST":
        League = request.form.get("League")
        Home = request.form.get("Home")
        Away = request.form.get("Away")
        Pitch = request.form.get("Pitch")
        Date = request.form.get("Date")
        Time = request.form.get("Time")
    seasons = Season.query.all()
    return render_template('addFixture.html',seasons=seasons)
@app.route('/Fixtures',methods=["GET", "POST"])
def fixtures():
    return "hello"
if __name__ == '__main__':
    app.run(debug=True)
