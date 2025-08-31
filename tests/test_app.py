import pytest
import json
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app
from models import TaskManager, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_task_data():
    return {
        "title": "Test Task",
        "description": "This is a test task"
    }

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_get_empty_tasks(client):
    """Test getting tasks when none exist"""
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []

def test_create_task(client, sample_task_data):
    """Test creating a new task"""
    response = client.post('/tasks', 
                          data=json.dumps(sample_task_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == sample_task_data['title']
    assert data['description'] == sample_task_data['description']
    assert data['status'] == 'pending'
    assert 'id' in data
    assert 'created_at' in data

def test_create_task_missing_title(client):
    """Test creating task without title fails"""
    response = client.post('/tasks',
                          data=json.dumps({"description": "No title"}),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

# Test the Task model directly
def test_task_creation():
    """Test Task model creation"""
    task = Task(1, "Test Task", "Description")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert task.status == "pending"

def test_task_to_dict():
    """Test Task model to_dict method"""
    task = Task(1, "Test Task")
    task_dict = task.to_dict()
    assert task_dict['id'] == 1
    assert task_dict['title'] == "Test Task"
    assert task_dict['status'] == "pending"

def test_task_manager():
    """Test TaskManager functionality"""
    manager = TaskManager()
    
    # Test creating task
    task = manager.create_task("Test Task", "Description")
    assert task.id == 1
    assert len(manager.get_all_tasks()) == 1
    
    # Test getting task by ID
    retrieved_task = manager.get_task_by_id(1)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"

