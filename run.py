# This is the entry point that initializes the flask app from __init__.py

from app import app

if __name__ == "__main__":
    
    # run flask app that is initialized (debug mode) 
    app.run(debug=True)