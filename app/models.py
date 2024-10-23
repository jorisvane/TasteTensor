from app import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cleaned_ingredients = db.Column(db.ARRAY(db.String), nullable=False)
    ingredients_vector = db.Column(db.ARRAY(db.Float), nullable=False)
