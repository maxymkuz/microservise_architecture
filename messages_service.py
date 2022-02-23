from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)


class TodoList(Resource):
    def get(self):
        return "not implemented, go nahui", 200

    def post(self):
        return "not implemented as well", 201
        # args = parser.parse_args()
        # todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        # todo_id = 'todo%i' % todo_id
        # TODOS[todo_id] = {'task': args['task']}
        # return TODOS[todo_id], 201


# Actually setup the Api resource routing here
api.add_resource(TodoList, '/')

if __name__ == '__main__':
    app.run(debug=True)
