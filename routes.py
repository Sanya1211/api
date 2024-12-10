from flask import Blueprint, request, jsonify, abort
from models import db, Recipe, User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

bp = Blueprint("recipes", __name__, url_prefix="/recipes")

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login and generate JWT token"""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        abort(400, description="Username and password are required")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        abort(401, description="Invalid username or password")

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

# Logout route to revoke the token
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout by revoking the token"""
    return jsonify(msg="Successfully logged out"), 200


# Recipe routes with JWT protection
@bp.route("/", methods=["GET"])
@jwt_required()
def get_all_recipes():
    """Отримати всі рецепти"""
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@bp.route("/<int:recipe_id>", methods=["GET"])
@jwt_required()
def get_recipe(recipe_id):
    """Отримати рецепт за ID"""
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())

@bp.route("/", methods=["POST"])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def delete_recipe(recipe_id):
    """Видалити рецепт за ID"""
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted"})
