from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    date = db.Column(db.String(50), nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Workout name must be at least 3 characters")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if not value:
            raise ValueError("Date is required")
        return value


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    muscle_group = db.Column(db.String(100), nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters")
        return value

    @validates("muscle_group")
    def validate_muscle_group(self, key, value):
        allowed = ["chest", "back", "legs", "shoulders", "arms", "core", "full body"]
        if value.lower() not in allowed:
            raise ValueError(f"muscle_group must be one of: {', '.join(allowed)}")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (
        CheckConstraint("sets > 0", name="check_sets_positive"),
        CheckConstraint("reps > 0 OR duration > 0", name="check_reps_or_duration"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer)
    duration = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("sets")
    def validate_sets(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Sets must be greater than 0")
        return value
