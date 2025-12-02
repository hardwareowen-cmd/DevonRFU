from app import db,app
from models import User

admin = User(email="leagueadmin@example.com")
admin.set_userpassword("password123")
admin.set_username("leagueadmin")
admin.set_adminLevel(2)
admin.set_userclub("none")
admin.set_usercreated_by("Program")
with app.app_context():
    db.session.add(admin)
    db.session.commit()

