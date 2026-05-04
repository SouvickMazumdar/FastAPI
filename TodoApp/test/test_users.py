from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_return_user(test_user):
    response=client.get("/user")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()[0]['username']=='codingwithsouvicktest' 
    assert response.json()[0]['email']=='codingwithsouvicktest@gmail.com' 
    assert response.json()[0]['first_name']=='Souvick'
    assert response.json()[0]['last_name']=='Mazumdar'
    assert response.json()[0]['role']=='admin'
    assert response.json()[0]['phone_number']=='(+91)-111-111'

def test_change_password_success(test_user):
    response=client.put("/user/change_password",json={"old_password":"testpassword","new_password":"newpassword","confirm_password":"newpassword"})
    assert response.status_code==status.HTTP_200_OK

def test_change_password_invalid_current_password(test_user):
    response=client.put("/user/change_password",json={"old_password":"wrongpassword","new_password":"newpassword","confirm_password":"newpassword"})
    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':'Wrong old Password'}

def test_change_phone_number_success(test_user):
    response=client.put("/user/update_phone_number?phone_number=2222222222")
    assert response.status_code==status.HTTP_204_NO_CONTENT


#  old_password: str
#     new_pasword: str= Field(min_length=6)
#     confirm_password: str
