from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from models import db, Recipe  
from routes import bp  
import time

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()  

def measure_query_time(query_func, *args, **kwargs):
    """Функція для вимірювання часу виконання запиту"""
    start_time = time.time()
    query_func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time

def test_insert(n):
    """Тестуємо вставку записів в базу даних"""
    recipes = [Recipe(
        name=f"Recipe {i}", 
        ingredients="Ingredient1, Ingredient2, Ingredient3", 
        instructions="Step 1, Step 2, Step 3", 
        preparation_time=30, 
        difficulty="Easy"
    ) for i in range(n)]
    db.session.bulk_save_objects(recipes)
    db.session.commit()

def test_select():
    """Тестуємо вибірку всіх записів з таблиці рецептів"""
    return Recipe.query.all()

def test_update():
    """Тестуємо оновлення записів"""
    recipe = Recipe.query.first()
    if recipe:  
        recipe.title = "Updated Recipe Title"  
        db.session.commit()

def test_delete():
    """Тестуємо видалення записів"""
    recipe = Recipe.query.first()
    if recipe: 
        db.session.delete(recipe)
        db.session.commit()

def benchmark_operations():
    """Виконуємо заміри для кожної операції з різною кількістю записів"""
    results = {}

    for n in [1000, 10000, 100000, 1000000]:
        print(f"Running tests with {n} records...")

        insert_time = measure_query_time(test_insert, n)
        results[f"Insert {n}"] = insert_time

        select_time = measure_query_time(test_select)
        results[f"Select {n}"] = select_time

        update_time = measure_query_time(test_update)
        results[f"Update {n}"] = update_time

        delete_time = measure_query_time(test_delete)
        results[f"Delete {n}"] = delete_time

    return results

def print_benchmark_results(results):
    """Вивести результати бенчмарків"""
    print("\nBenchmark Results:")
    for operation, time_taken in results.items():
        print(f"{operation}: {time_taken:.5f} seconds")

app.register_blueprint(bp)  

if __name__ == '__main__':
    with app.app_context():
        benchmark_results = benchmark_operations()
        print_benchmark_results(benchmark_results)

    app.run(debug=True)
