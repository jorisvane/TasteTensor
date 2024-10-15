from app import app, db
from flask import jsonify
from app.models import Recipe  # Assuming you have a Recipe model

@app.route('/test-db')
def test_db():
    try:
        # Query all records in the recipes table (should return an empty list if the table is empty)
        recipes = Recipe.query.all()
        if recipes:
            return jsonify([recipe.title_image for recipe in recipes])
        else:
            return jsonify({"message": "No records found in the database."})
    except Exception as e:
        # Catch any error and return a message
        return jsonify({"error": str(e)})