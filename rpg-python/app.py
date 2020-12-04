from flask import Flask
from flask_restful import Api

from resources.sheet import SheetListResource, SheetResource, SheetPublishResource

app = Flask(__name__)
api = Api(app)

api.add_resource(SheetListResource, '/sheets')
api.add_resource(SheetResource, '/sheets/<int:sheet_id>')
api.add_resource(SheetPublishResource, '/sheets/<int:sheet_id>/publish')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
