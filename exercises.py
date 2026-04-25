from flask import Blueprint, request, jsonify
from models import db, Exercise
from schemas import ExerciseSchema

exercise_bp = Blueprint("exercises", __name__)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)


@exercise_bp.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@exercise_bp.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json() or {}
    errors = exercise_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        exercise = Exercise(name=data["name"], muscle_group=data["muscle_group"])
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@exercise_bp.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@exercise_bp.route("/exercises/<int:id>", methods=["PATCH"])
def update_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    data = request.get_json() or {}
    try:
        if "name" in data:
            exercise.name = data["name"]
        if "muscle_group" in data:
            exercise.muscle_group = data["muscle_group"]
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@exercise_bp.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return {}, 204
