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
