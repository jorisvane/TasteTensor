import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import both app and db from your app module
from app import app, db

# Create the tables within the app context
with app.app_context():
    db.create_all()
    print("Tables created successfully!")

