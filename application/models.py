from application import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) #change integer to string for username
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(16))
    name = db.Column(db.String(128))
    gender = db.Column(db.String(1))
    budget = db.Column(db.Float)
    weight = db.Column(db.Float)
    weight_goal = db.Column(db.Float)
    avg_cals_burned = db.Column(db.Float)
    location = db.Column(db.String(128))
    notes = db.Column(db.String(128), index=True, unique=False)

    def __init__(self, username, password, name, gender, budget, weight, weight_goal, avg_cals_burned, location, notes):
        self.name = name
        self.username = username
        self.password = password
        self.gender = gender
        self.budget = budget
        self.weight = weight
        self.weight_goal = weight_goal
        self.avg_cals_burned = avg_cals_burned
        self.location = location
        self.notes = notes

    def __repr__(self):
        return '<User %r>' % self.notes
