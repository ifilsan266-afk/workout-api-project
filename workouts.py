from flask import Blueprint, request, jsonify
from models import db, Workout, WorkoutExercise, Exercise
from schemas import WorkoutSchema, WorkoutExerciseSchema

workout_bp = Blueprint("workouts", __name__)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
we_schema = WorkoutExerciseSchema()


@workout_bp.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@workout_bp.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json() or {}
    errors = workout_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        workout = Workout(name=data["name"], date=data["date"])
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@workout_bp.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@workout_bp.route("/workouts/<int:id>", methods=["PATCH"])
def update_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json() or {}
    try:
        if "name" in data:
            workout.name = data["name"]
        if "date" in data:
            workout.date = data["date"]
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@workout_bp.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return {}, 204


@workout_bp.route("/workout-exercises", methods=["POST"])
def create_workout_exercise():
    data = request.get_json() or {}

    workout = db.session.get(Workout, data.get("workout_id"))
    exercise = db.session.get(Exercise, data.get("exercise_id"))

    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    errors = we_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        we = WorkoutExercise(
            workout_id=data["workout_id"],
            exercise_id=data["exercise_id"],
            sets=data["sets"],
            reps=data.get("reps"),
            duration=data.get("duration"),
        )
        db.session.add(we)
        db.session.commit()
        return jsonify(we_schema.dump(we)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
