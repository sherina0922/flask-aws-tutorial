from application import db
from application.models import User, RecommendedRecipe

db.create_all()

print("DB created.")
