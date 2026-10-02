import requests 
import uuid
import pytest
from app.main import app
from sqlalchemy.orm import sessionmaker
from fastapi.encoders import jsonable_encoder
from app.core.database import get_session
from app.tests.user_test import client
from app.routers.groups import create_group, join_group, add_user_to_group
from app.models.group_model import Group

group_url =  '/groups'

@pytest.fixture
def group():
    return Group(group_name='test_group',
                 group_description='testing')
    

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
    
def test_create_group():
    url = group_url + '/create'
    
    response = client.post(url,
                           json=jsonable_encoder(group))
    assert response.status_code == 200
    
    
def test_add_user_to_group():
    url = group_url + '/add-user'
    ...
    
def test_join_group():
    ...
    