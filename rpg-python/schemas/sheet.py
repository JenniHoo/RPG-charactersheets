from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema


class StatisticsSchema(Schema):
    STR = fields.Int()
    DEX = fields.Int()
    INT = fields.Int()


class SheetSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    race = fields.String(validate=[validate.Length(max=100)])
    hp = fields.Int()
    statistics = fields.Nested(StatisticsSchema, only=['STR', 'DEX', 'INT'])

    is_publish = fields.Boolean(dump_only=True)
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}

        return data
