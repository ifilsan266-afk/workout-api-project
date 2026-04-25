from flask import Flask
from flask_migrate import Migrate
from models import db
from workouts import workout_bp
from exercises import exercise_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
