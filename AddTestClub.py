from app import db,app
from models import League

league = League(name="test")
league.set_LeagueAgeGroup("u7")
league.set_LeagueSeason("25/26")
with app.app_context():
    db.session.add(league)
    db.session.commit()
