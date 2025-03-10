from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()  # Load env vars

app = Flask(__name__)
CORS(app)

# PostgreSQL connection URI from environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ✅ Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# ✅ Create tables on first run
with app.app_context():
    db.create_all()

# ✅ Root route for confirmation
@app.route("/")
def home():
    return "✅ Study Planner Backend is Running!"

# ✅ Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "name": t.name, "completed": t.completed} for t in tasks])

# ✅ Add new task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    new_task = Task(name=data["name"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "name": new_task.name, "completed": new_task.completed})

# ✅ Update task status
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    task = Task.query.get(task_id)
    if task:
        task.completed = data["complete d"]
        db.session.commit()
        return jsonify({"id": task.id, "name": task.name, "completed": task.completed})
    return jsonify({"error": "Task not found"}), 404

# ✅ Delete task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404

# ✅ Clear all tasks
@app.route("/tasks", methods=["DELETE"])
def clear_all_tasks():
    try:
        num_deleted = db.session.query(Task).delete()
        db.session.commit()
        return jsonify({"message": f"{num_deleted} tasks cleared!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
 