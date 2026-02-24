
from app import schemas
from .database import client,session
import pytest


@pytest.fixture()
def test_user(client):
     user_data = {"username":"test","email":"test1@gmail.com","password":"password!123"}
     response = client.post('/users', json=user_data)
     new_user = response.json()
     new_user['password'] =  user_data['password']
     print (new_user)
     return new_user




def test_root(client):
    response = client.get('/')
    print(response.json()) 

# Test create user route
def test_create_user(client):
    response = client.post('/users', json={"username":"test","email":"test@gmail.com","password":"password!123"})
    print(response.status_code)
    print(response.json())
    
    assert response.status_code == 201

    new_user = schemas.UserResponse(**response.json())


# Test UserLogin
def test_login_user(test_user,client):
    response = client.post('/login', data = {"username":test_user['email'],"password":test_user['password']})
    assert response.status_code == 200