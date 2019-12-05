from application import db
from application.models import User, RecommendedRecipe, RecipeMongoSetUp, ProduceMongoSetUp

db.create_all()
RecipeMongoSetUp()
ProduceMongoSetUp()

print("DBs created.")
