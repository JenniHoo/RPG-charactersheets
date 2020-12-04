from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.sheet import Sheet, sheet_list


class SheetListResource(Resource):

    def get(self):

        data = []

        for sheet in sheet_list:
            if sheet.is_publish is True:
                data.append(sheet.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        sheet = Sheet(name=data['name'],
                      race=data['race'],
                      hp=int(data['hp']),
                      statistics=data['statistics'])

        sheet_list.append(sheet)

        return sheet.data, HTTPStatus.CREATED


class SheetResource(Resource):

    def get(self, sheet_id):
        sheet = next((sheet for sheet in sheet_list if sheet.id == sheet_id and sheet.is_publish == True), None)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        return sheet.data, HTTPStatus.OK

    def put(self, sheet_id):
        data = request.get_json()

        sheet = next((sheet for sheet in sheet_list if sheet.id == sheet_id), None)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        sheet.name = data['name']
        sheet.race = data['race']
        sheet.hp = int(data['hp'])
        sheet.statistics = data['statistics']

        return sheet.data, HTTPStatus.OK

    def delete(self, sheet_id):
        sheet = next((sheet for sheet in sheet_list if sheet.id == sheet_id), None)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        sheet_list.remove(sheet)

        return {}, HTTPStatus.NO_CONTENT


class SheetPublishResource(Resource):

    def put(self, sheet_id):
        sheet = next((sheet for sheet in sheet_list if sheet.id == sheet_id), None)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        sheet.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, sheet_id):
        sheet = next((sheet for sheet in sheet_list if sheet.id == sheet_id), None)

        if sheet is None:
            return {'message': 'sheet not found'}, HTTPStatus.NOT_FOUND

        sheet.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
