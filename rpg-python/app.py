from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

sheets = [
    {
        'id': 1,
        'name': 'Frodo',
        'race': 'Hobbit',
        'hp': 10,
        'statistics': {
            'STR': 5,
            'DEX': 5,
            'INT': 6
        }
    },
    {
        'id': 2,
        'name': 'Sam',
        'race': 'Hobbit',
        'hp': 12,
        'statistics': {
            'STR': 6,
            'DEX': 5,
            'INT': 5
        }
    }
]


@app.route('/sheets', methods=['GET'])
def get_sheets():
    return jsonify({'data': sheets})


@app.route('/sheets/<int:sheet_id>', methods=['GET'])
def get_sheet(sheet_id):
    sheet = next((sheet for sheet in sheets if sheet['id'] == sheet_id), None)

    if sheet:
        return jsonify(sheet)

    return jsonify({'message': 'sheet not found'}), HTTPStatus.NOT_FOUND


@app.route('/sheets', methods=['POST'])
def create_sheet():
    data = request.get_json()

    name = data['name']
    race = data['race']
    hp = data['hp']
    strength = data['statistics']['STR']
    dexterity = data['statistics']['DEX']
    intelligence = data['statistics']['INT']

    sheet = {
        'id': len(sheets) + 1,
        'name': name,
        'race': race,
        'hp': int(hp),
        'statistics': {
            'STR': strength,
            'DEX': dexterity,
            'INT': intelligence
        }
    }

    sheets.append(sheet)

    return jsonify(sheet), HTTPStatus.CREATED


@app.route('/sheets/<int:sheet_id>', methods=['PUT'])
def update_sheet(sheet_id):
    sheet = next((sheet for sheet in sheets if sheet['id'] == sheet_id), None)

    if not sheet:
        return jsonify({'message': 'sheet not found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    sheet.update(
        {
            'name': data['name'],
            'race': data['race'],
            'hp': int(data['hp']),
            'statistics': {
                'STR': data['statistics']['STR'],
                'DEX': data['statistics']['DEX'],
                'INT': data['statistics']['INT']
            }
        }
    )

    return jsonify(sheet)


@app.route('/sheets/<int:sheet_id>', methods=['DELETE'])
def delete_sheet(sheet_id):
    sheet = next((sheet for sheet in sheets if sheet['id'] == sheet_id), None)

    if not sheet:
        return jsonify({'message': 'sheet not found'}), HTTPStatus.NOT_FOUND

    sheets.remove(sheet)

    return '', HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run()
