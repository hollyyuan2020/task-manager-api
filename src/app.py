from flask import Flask, jsonify, request
from models import TaskManager

app = Flask(__name__)
task_manager = TaskManager()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Task Manager API is running"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = task_manager.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    task = task_manager.create_task(
        title=data['title'],
        description=data.get('description', '')
    )
    return jsonify(task.to_dict()), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

