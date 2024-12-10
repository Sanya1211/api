from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  
    ingredients = db.Column(db.Text, nullable=False)  
    instructions = db.Column(db.Text, nullable=False)  
    preparation_time = db.Column(db.Integer, nullable=False) 
    difficulty = db.Column(db.String(20), nullable=False)  

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "preparation_time": self.preparation_time,
            "difficulty": self.difficulty
        }
