# Flask Web-API with jsonschema validation example

## Introduction

If a web-api is needed in a minimal, quick, and efficient manner a very
nice setup is to use Flask and jsonschema.

## Jsonschema 

Jsonschema is great because it not only describes your data format but
it will provide complete structural validation.

**A basic example**
> Note: this example is taken from the python jsonschema docs 

```python
from jsonschema import validate

# A sample schema, like what we'd get from json.load()
schema = {
    "type" : "object",
    "properties" : {
    "price" : {"type" : "number"},
    "name" : {"type" : "string"},
    },
}

# If no exception is raised by validate(), the instance is valid.
validate({"name" : "Eggs", "price" : 34.99}, schema)

validate({"name" : "Eggs", "price" : "Invalid"}, schema)

Traceback (most recent call last):
...
ValidationError: 'Invalid' is not of type 'number'
```
https://python-jsonschema.readthedocs.org/en/latest/

## Implementation with Flask

All the magic is done via a decorator on the flask route which specifies
a jsonschema to validate against. The decorator will validate the schema and return the decorated
function or it will return an error.

**Example Decorator**

```python
from schemas import input_foo_schema

def validate_schema(schema):
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

# Decorated route with 
@app.route('/foo', methods=['POST'])
@validate_schema(input_foo_schema)
def foo():
    ...
    return jsonify(dict(message='success!))

```

## The TODO schema

[schemas\todo_input_schema.py](schemas/input_todo_schema.py)

```
input_todo_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "input-todo-schema",
    "description": "Schema of post data for creating a new todo \
                    in the todo app.",
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "description": "The unique id of the todo:",
            "maxLength": 255
        },
        "userId": {
            "type": "string",
            "description": "The unique id of user.",
            "maxLength": 255
        },
        "title": {
            "type": "string",
            "description": "The title of the todo",
            "maxLength": 255
        },
        "completed": {
            "type": "boolean",
            "description": "If the todo is completed or not",
        }
    },
    "additionalProperties": False,
    "required": ["userId", "title"]
}

```

**Example Error**

A post request to the /todos endpoint without the required userId field.

```
{
  "errors": [
    "'userId' is a required property"
  ],
  "message": "invalid input",
  "success": false
}
```

## Documentation with Sphinx

If you would like that route to show up in your documentation and you
are using sphinx you can do this easily by adding `sphinxcontrib.autohttp.flask`
to your sphinx extensions.

Within your documentation you can then specify what endpoints you want documented.

**Example**

```
.. autoflask:: app:create_app()
   :undoc-static:
   :endpoints: foo
   :include-empty-docstring:
```

You can then spruce up your route docstring to include the jsonschema 

**Example**

```python
@app.route('/foo', methods=['POST'])
@validate_schema(input_foo_schema)
def add_todo():
    """Save a new foo.

        **Example output**

        .. code-block:: http

           http/1.1 200 ok
           vary: accept
           content-type: application/json

           {
               "message": "Success",
           }

        :statuscode  200: Success
        :statuscode  406: Not Acceptable (validation error)

        **Input schema:**

        .. literalinclude:: /../../schemas/input_foo_schema_.py
           :lines: 1-30
```

**Example Docs**

![Example Sphinx documentation](http://i.imgur.com/j7rnUL1.png)

# Conclusion

With jsonschema and flask you can get a web-api with proper
validation of inputs with specific error messages indicating what
was wrong with a request. You can also add in a sphinx extension and have
web-api docs with very little effort.

### Attributions
Thanks a lot for navilan for first introducing me to this awesome way
of creating a web api.
