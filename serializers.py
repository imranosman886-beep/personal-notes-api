from marshmallow import Schema, fields, validate


# USER SCHEMAS

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()


class SignupSchema(Schema):
    username = fields.String(
        required=True,
        validate=validate.Length(min=1, max=80)
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=8)
    )
    password_confirmation = fields.String(required=True, load_only=True)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


# NOTE SCHEMAS

class NoteSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    content = fields.String()
    user_id = fields.Integer(dump_only=True)
    category_id = fields.Integer(allow_none=True)
    category = fields.Nested(
        "CategorySchema",
        allow_none=True,
        dump_only=True
    )
    created_at = fields.DateTime(dump_only=True)


class NoteInputSchema(Schema):
    title = fields.String(
        required=True,
        validate=validate.Length(min=1, max=120)
    )
    content = fields.String(
        required=True,
        validate=validate.Length(min=1)
    )
    category_id = fields.Integer(allow_none=True)


# CATEGORY SCHEMAS

class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    user_id = fields.Integer(dump_only=True)


class CategoryInputSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=80)
    )