from flask import Blueprint, request, jsonify, abort
from models import db, Recipe

bp = Blueprint("recipes", __name__, url_prefix="/recipes")

@bp.route("/", methods=["GET"])
def get_all_recipes():
    """Отримати всі рецепти"""
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@bp.route("/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    """Отримати рецепт за ID"""
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())

@bp.route("/", methods=["POST"])
def create_recipe():
    """Створити новий рецепт"""
    data = request.json
    required_fields = ["name", "ingredients", "instructions", "preparation_time", "difficulty"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Field '{field}' is required")
    
    new_recipe = Recipe(**data)
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201

@bp.route("/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    """Оновити рецепт за ID"""
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.json
    for key, value in data.items():
        if hasattr(recipe, key):
            setattr(recipe, key, value)
    db.session.commit()
    return jsonify(recipe.to_dict())

@bp.route("/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    """Видалити рецепт за ID"""
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted"})
