import requests
import pytest
from app.schemas.user_schema import UserCreate, UserBase

URL = 'http://127.0.0.1:8000/user'

    
@pytest.fixture
def user():
    return UserBase(username='L',
                        password='12345')

def test_register_user():
    new_user = UserCreate(username='New_user',
                        password='12345',
                        email='ksdfenc@gmail.com')
    url = URL + '/register'
    
    response = requests.post(url, json=new_user.model_dump())
    
    assert response.status_code == 200

def test_registered_user():
    registerd_user = UserCreate(username='L',
                        password='12345',
                        email='ksdfenc@gmail.com')
    url = URL + '/register'
    
    response = requests.post(url, json=registerd_user.model_dump())
    
    assert response.status_code == 403

def test_login_user(user: UserBase):
    
    url = URL + '/login'
    print(url)
    
    print(user.model_dump())
    
    response = requests.post(url, json=user.model_dump())
    
    assert response.status_code == 200


