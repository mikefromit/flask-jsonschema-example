import json
from functools import wraps

from flask import Flask, jsonify, abort, request

from jsonschema import Draft4Validator
from schemas.input_todo_schema import input_todo_schema


def validate_schema(schema):
    """Decorator that performs schema validation on the JSON post data in
    the request and returns an error response if validation fails.  It
    calls the decorated function if validation succeeds.

    :param schema: Schema that represents the expected input.

    """
    validator = Draft4Validator(schema)

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            input = request.get_json(force=True)
            errors = [error.message for error in validator.iter_errors(input)]
            if errors:
                response = jsonify(dict(success=False,
                                        message="invalid input",
                                        errors=errors))
                response.status_code = 406
                return response
            else:
                return fn(*args, **kwargs)
        return wrapped
    return wrapper


def create_app():

    settings = {
        'DEBUG': True,
    }

    app = Flask(__name__)
    app.config.update(settings)

    return app

app = create_app()


def get_todos():
    with open('todos.json', 'r') as infile:
        todos = json.load(infile)

    return todos


def save_todo(todo):
    todos = get_todos()
    with open('todos.json', 'w') as outfile:
        todos.append(todo)
        json.dump(todos, outfile, sort_keys=True, indent=4)

    return


@app.route('/todos', methods=['GET'])
def list_todos():
    todos = get_todos()
    return jsonify(dict(todos=todos))


@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todos = get_todos()

    for todo in todos:
        if todo['id'] == id:
            return jsonify(todo)

    return abort(404)


@app.route('/todos', methods=['POST'])
@validate_schema(input_todo_schema)
def add_todo():
    """Save a new todo.

        **Example output**

        .. code-block:: http

           http/1.1 200 ok
           vary: accept
           content-type: application/json

           {
               "message": "todo saved.",
           }

        :statuscode  200: Success
        :statuscode  406: Not Acceptable (validation error)

        **Input schema:**

        .. literalinclude:: /../../schemas/input_todo_schema.py
           :lines: 1-30
    """
    posted = request.get_json()
    todos_len = len(get_todos())
    todo = dict(
        id = todos_len + 1,
        userId=posted['userId'],
        title=posted['title'],
        completed=posted['completed'] if 'completed' in posted else False
    )
    save_todo(todo)
    return jsonify(dict(msg='todo saved'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
