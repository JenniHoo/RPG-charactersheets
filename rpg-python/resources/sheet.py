from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.sheet import Sheet
from schemas.sheet import SheetSchema

sheet_schema = SheetSchema()
sheet_list_schema = SheetSchema(many=True)


class SheetListResource(Resource):

    def get(self):

        sheets = Sheet.get_all_published()

        return sheet_list_schema.dump(sheets).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = sheet_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        sheet = Sheet(**data)
        sheet.user_id = current_user
        sheet.save()

        return sheet_schema.dump(sheet).data, HTTPStatus.CREATED


class SheetResource(Resource):

    @jwt_optional
    def get(self, sheet_id):

        sheet = Sheet.get_by_id(sheet_id=sheet_id)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if sheet.is_publish == False and sheet.user_id != current_user:
            return {'message': 'access not allowed'}, HTTPStatus.FORBIDDEN

        return sheet.data(), HTTPStatus.OK

    @jwt_required
    def patch(self, sheet_id):

        json_data = request.get_json()

        data, errors = sheet_schema.load(data=json_data, partial=('name', ))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        sheet = Sheet.get_by_id(sheet_id=sheet_id)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != sheet.user_id:
            return {'message': 'access is not allowed'}, HTTPStatus.FORBIDDEN

        sheet.name = data.get('name') or sheet.name
        sheet.race = data.get('race') or sheet.race
        sheet.hp = data.get('hp') or sheet.hp
        sheet.statistics = data.get('statistics') or sheet.statistics

        sheet.save()

        return sheet_schema.dump(sheet).data, HTTPStatus.OK

    @jwt_required
    def delete(self, sheet_id):

        sheet = Sheet.get_by_id(sheet_id=sheet_id)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != sheet.user_id:
            return {'message': 'access is not allowed'}, HTTPStatus.FORBIDDEN

        sheet.delete()

        return {}, HTTPStatus.NO_CONTENT


class SheetPublishResource(Resource):

    @jwt_required
    def put(self, sheet_id):
        sheet = Sheet.get_by_id(sheet_id=sheet_id)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != sheet.user_id:
            return {'message': 'access is not allowed'}, HTTPStatus.FORBIDDEN

        sheet.is_publish = True
        sheet.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, sheet_id):
        sheet = Sheet.get_by_id(sheet_id=sheet_id)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != sheet.user_id:
            return {'message': 'access is not allowed'}, HTTPStatus.FORBIDDEN

        sheet.is_publish = False
        sheet.save()

        return {}, HTTPStatus.NO_CONTENT
