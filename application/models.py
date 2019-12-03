from application import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) #change integer to string for username
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(16))
    name = db.Column(db.String(128))
    gender = db.Column(db.String(1))
    budget = db.Column(db.Float)
    calories = db.Column(db.Float)
    avg_cals_burned = db.Column(db.Float)
    location = db.Column(db.String(128))

    def __init__(self, username, password, name, gender, budget, calories, avg_cals_burned, location):
        self.name = name
        self.username = username
        self.password = password
        self.gender = gender
        self.budget = budget
        self.calories = calories
        self.avg_cals_burned = avg_cals_burned
        self.location = location

    def __repr__(self):
        return '<User %r>' % self.name

class RecommendedRecipe(db.Model):
    __tablename__ = 'recommendedrecipes'
    recipe_id = db.Column(db.Integer, primary_key=True) #change integer to string for username
    user_id = db.Column(db.String(128), primary_key=True)
    recipe_name = db.Column(db.String(128))
    date_recommended = db.Column(db.String(128))

    def __init__(self, recipe_id, user_id, recipe_name, date_recommended):
        self.recipe_id = recipe_id
        self.user_id = user_id
        self.date_recommended = date_recommended
        self.recipe_name = recipe_name

    def __repr__(self):
        return '<Recipe %r>' % self.recipe_name
