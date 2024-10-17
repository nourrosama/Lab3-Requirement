from flask import Flask, Blueprint, request, jsonify
import token

app = Flask(__name__)

TOKEN = "mysecrettoken"

todos = []

@app.before_request
def authenticate_token():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401
    
# 1 returns all todos in the todos list.
@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

# 2 search for a todo by its id
@app.route("/todos/<int:id>", methods=["GET"])
def get_todo_by_id(id):
    todo = next((t for t in todos if t["id"] == id), None)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo)


# 3
@app.route("/todos", methods=["POST"])
def create_todo():
    todo = {
        "id": len(todos) + 1,
        "title": request.json.get("title"),
        "completed": request.json.get("completed", False),
    }
    todos.append(todo)
    return jsonify (todo), 201


# 4
@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    todo = next((t for t in todos if t["id"] == id), None)
    if todo is None:    
        return jsonify({"error": "Todo not found"}), 404
    todo["title"] = request.json.get ("title", todo["title"])
    todo ["completed"] = request.json.get("completed", todo["completed"])
    return jsonify (todo)


# 5
@app.route("/todos/<int:id>", methods= ["DELETE"])
def delete_todo(id):
    global todos
    todos = [t for t in todos if t["id"] != id]
    return '', 204


@app.errorhandler (404)
def not_found(e) :
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=3000)