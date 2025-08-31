from flask import Blueprint, jsonify, request
from models import TaskManager

# This file will contain additional route definitions
# to be imported into the main app

api = Blueprint('api', __name__)

def register_routes(app, task_manager):
    """Register additional routes with the Flask app"""
    
    @app.route('/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        task = task_manager.get_task_by_id(task_id)
        if task:
            return jsonify(task.to_dict())
        return jsonify({"error": "Task not found"}), 404
    
    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        task = task_manager.get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        # Update task fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            if data['status'] in ['pending', 'in_progress', 'completed']:
                task.status = data['status']
            else:
                return jsonify({"error": "Invalid status"}), 400
        
        return jsonify(task.to_dict())
    
    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        if task_manager.delete_task(task_id):
            return '', 204
        return jsonify({"error": "Task not found"}), 404
    
    @app.route('/tasks/status/<status>', methods=['GET'])
    def get_tasks_by_status(status):
        if status not in ['pending', 'in_progress', 'completed']:
            return jsonify({"error": "Invalid status"}), 400
        
        all_tasks = task_manager.get_all_tasks()
        filtered_tasks = [task for task in all_tasks if task.status == status]
        return jsonify([task.to_dict() for task in filtered_tasks])

