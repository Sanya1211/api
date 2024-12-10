from flask import Flask
from models import db
from routes import bp, auth_bp
from config import Config
from flask_jwt_extended import JWTManager

def create_default_user():
    """Add a default user if not already present"""
    from werkzeug.security import generate_password_hash
    from models import User

    user = User.query.filter_by(username="username").first()
    if not user:
        hashed_password = generate_password_hash("password")
        default_user = User(username="username", password=hashed_password)
        db.session.add(default_user)
        db.session.commit()
        print("Default user created")
    else:
        print("Default user already exists")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    jwt = JWTManager(app) 

    with app.app_context():
        db.create_all() 
        create_default_user()  

    app.register_blueprint(bp)  
    app.register_blueprint(auth_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
