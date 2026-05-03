from .utils import *
from fastapi import status
from ..routers.admin import get_db, get_current_user
app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response=client.get("/admin/todo")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==[{
        'title':"Learn to code !!!",
        'description':"Need to learn everyday!!!",
        'priority':5,
        'complete':False,
        'owner_id':1,
        'id':1
        }]                                                                                       