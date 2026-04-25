from marshmallow import Schema, fields, validate, validates, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    muscle_group = fields.Str(required=True)

    @validates("muscle_group")
    def validate_muscle_group(self, value):
        allowed = ["chest", "back", "legs", "shoulders", "arms", "core", "full body"]
        if value.lower() not in allowed:
            raise ValidationError(f"muscle_group must be one of: {', '.join(allowed)}")


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    sets = fields.Int(required=True, validate=validate.Range(min=1))
    reps = fields.Int(load_default=None)
    duration = fields.Int(load_default=None)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates("sets")
    def validate_sets(self, value):
        if value <= 0:
            raise ValidationError("Sets must be greater than 0")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))
    date = fields.Str(required=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)
