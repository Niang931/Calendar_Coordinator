import requests 
import uuid
import pytest
from app.main import app
from datetime import date
from app.core.database import get_session, sessionmaker, engine
from app.tests.user_test import client, test_login_user, user_url
from app.schemas.task_schema import Task
from app.schemas.user_schema import UserBase
from fastapi.encoders import jsonable_encoder

test_url = '/tasks/'

@pytest.fixture
def task():
    task = Task(title='New',
                start_date=date(2026, 9, 25),
                start_time='13:00',
                duration=1.00)
    return task

@pytest.fixture
def existing_user():
    return UserBase(username='string',
                        password='string')

@pytest.fixture
def setup_db_override():
    # This function acts as the replacement generator
    def _override_get_db():
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    # Apply the override before the test runs
    app.dependency_overrides[get_session] = _override_get_db
    yield
    # Clean up the override after the test finishes
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(existing_user: UserBase):
    """Logs in the user and returns the Authorization header."""

    url = f"{user_url}/logiin" 
    
    response = client.post(url, json=existing_user.model_dump())
    assert response.status_code == 200

    token = response.json().get("access_token") 
    
    return {"Authorization": f"Bearer {token}"}


def test_create_task(auth_headers, task: Task, user_id: str = 'd9757e7a-3f10-4096-84ac-6a1d3f1b0c10'):
    url = f"{test_url}{user_id}/create"
    
    # 4. Pass the auth_headers fixture into the client headers
    response = client.post(
        url, 
        json=jsonable_encoder(task), 
        headers=auth_headers
    )
    
    assert response.status_code == 200
