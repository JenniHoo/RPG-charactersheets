from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.sheet import Sheet


class SheetListResource(Resource):

    def get(self):

        sheets = Sheet.get_all_published()

        data = []

        for sheet in sheets:
            data.append(sheet.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()
        sheet = Sheet(name=json_data['name'],
                      race=json_data['race'],
                      hp=int(json_data['hp']),
                      statistics=json_data['statistics'],
                      user_id=current_user)

        sheet.save()

        return sheet.data(), HTTPStatus.CREATED


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
    def put(self, sheet_id):

        json_data = request.get_json()

        sheet = Sheet.get_by_id(sheet_id=sheet_id)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != sheet.user_id:
            return {'message': 'access is not allowed'}, HTTPStatus.FORBIDDEN

        sheet.name = json_data['name']
        sheet.race = json_data['race']
        sheet.hp = int(json_data['hp'])
        sheet.statistics = json_data['statistics']

        sheet.save()

        return sheet.data(), HTTPStatus.OK

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
