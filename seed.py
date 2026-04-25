from app import create_app
from models import db, Workout, Exercise, WorkoutExercise

app = create_app()

with app.app_context():
    # Clear existing data
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    # Seed exercises
    push_up = Exercise(name="Push Up", muscle_group="chest")
    squat = Exercise(name="Squat", muscle_group="legs")
    deadlift = Exercise(name="Deadlift", muscle_group="back")
    plank = Exercise(name="Plank", muscle_group="core")
    shoulder_press = Exercise(name="Shoulder Press", muscle_group="shoulders")

    db.session.add_all([push_up, squat, deadlift, plank, shoulder_press])
    db.session.commit()

    # Seed workouts
    workout1 = Workout(name="Morning Strength", date="2026-04-20")
    workout2 = Workout(name="Leg Day", date="2026-04-21")
    workout3 = Workout(name="Full Body Blast", date="2026-04-22")

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()

    # Seed workout exercises
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=push_up.id, sets=3, reps=15)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=shoulder_press.id, sets=3, reps=10)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=squat.id, sets=4, reps=12)
    we4 = WorkoutExercise(workout_id=workout2.id, exercise_id=deadlift.id, sets=3, reps=8)
    we5 = WorkoutExercise(workout_id=workout3.id, exercise_id=plank.id, sets=3, duration=60)
    we6 = WorkoutExercise(workout_id=workout3.id, exercise_id=push_up.id, sets=4, reps=20)

    db.session.add_all([we1, we2, we3, we4, we5, we6])
    db.session.commit()

    print("Database seeded successfully!")
