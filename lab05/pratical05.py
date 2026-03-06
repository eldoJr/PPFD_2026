from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory storage
tasks = []
next_id = 1


def find_task(task_id):
    return next((t for t in tasks if t["id"] == task_id), None)


# GET all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks, "total": len(tasks)}), 200


# GET single task
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = find_task(task_id)
    if not task:
        abort(404, description=f"Task {task_id} not found")
    return jsonify(task), 200


# CREATE task
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    if not data or not data.get("title"):
        abort(400, description="'title' field is required")

    task = {
        "id": next_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "done": data.get("done", False),
    }
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


# UPDATE task (full or partial)
@app.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        abort(404, description=f"Task {task_id} not found")

    data = request.get_json()
    if not data:
        abort(400, description="JSON body required")

    if "title" in data:
        task["title"] = data["title"]
    if "description" in data:
        task["description"] = data["description"]
    if "done" in data:
        task["done"] = bool(data["done"])

    return jsonify(task), 200


# DELETE task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        abort(404, description=f"Task {task_id} not found")

    tasks.remove(task)
    return jsonify({"message": f"Task {task_id} deleted successfully"}), 200


# DELETE all tasks
@app.route("/tasks", methods=["DELETE"])
def delete_all_tasks():
    tasks.clear()
    return jsonify({"message": "All tasks deleted"}), 200


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify({"error": str(e.description)}), e.code


if __name__ == "__main__":
    app.run(debug=True, port=5000)