import requests 
import uuid
import pytest
from app.schemas.task_schema import Task

URL = 'http://127.0.0.1:8000/tasks'

@pytest.fixture
def task():
    user_id = ''
    task = Task(title='New',
                start_date='2026-09-21',
                duration=1.00)
    return user_id, task
    
def test_create_task(user_id: uuid.UUID, task: Task):
    url = URL + user_id + '/create'
    
    response = requests.post(url, json=task.model_dump())
    
    assert response.status_code == 200
