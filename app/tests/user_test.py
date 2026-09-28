import requests
import pytest
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_session, engine
from app.schemas.user_schema import UserCreate, UserBase


client = TestClient(app)

user_url = '/user'

@pytest.fixture
def existing_user():
    return UserBase(username='string',
                        password='string')
    
@pytest.fixture(autouse=True)
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



def test_register_user():
    new_user = UserCreate(username='test_user1',
                        password='12345',
                        email='ksdfenc@gmail.com')
    url = user_url + '/register'
    
    response = client.post(url, json=new_user.model_dump())
    
    assert response.status_code == 200

def test_registered_user():
    registerd_user = UserCreate(username='string',
                        password='string',
                        email='ksdfenc@gmail.com')
    url = user_url + '/register'
    
    response = client.post(url, json=registerd_user.model_dump())
    
    assert response.status_code == 403

def test_login_user(existing_user: UserBase):
    
    url = user_url + '/logiin'

    response = client.post(url, json=existing_user.model_dump())
    
    assert response.status_code == 200


