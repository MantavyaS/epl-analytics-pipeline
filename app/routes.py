from app import app
from flask import jsonify
from analytics.best_attack import get_best_attack
from analytics.best_defence import get_best_defence
from analytics.movement import get_movement
from analytics.points_gained import get_points_gained
from analytics.topscorer_efficiency import get_topscorer_efficiency

@app.route("/")
def home():
    return {"message": "Prem Analytics API running"}

@app.route("/best-attack")
def best_attack():
    results = get_best_attack()
    return jsonify(results)

@app.route("/best-defence")
def best_defence():
    results = get_best_defence()
    return jsonify(results)

@app.route("/movement")
def movement():
    results = get_movement()
    return jsonify(results)

@app.route("/points-gained")
def points_gained():
    results = get_points_gained()
    return jsonify(results)

@app.route("/topscorer-efficiency")
def topscorer_efficiency():
    results = get_topscorer_efficiency()
    return jsonify(results)
