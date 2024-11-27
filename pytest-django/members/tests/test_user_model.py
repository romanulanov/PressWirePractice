import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


#Написать автотест, который положит в БД учётку пользователя, а затем проверит что она там появилась
@pytest.mark.django_db
def test_create_user():
    username = "1234"
    email = "testuser@example.com"
    password = "securepassword123"
    
    
    user = User.objects.create_user(username=username, email=email, password=password)

    assert User.objects.filter(username=username).exists()

    saved_user = User.objects.get(username=username)
    assert saved_user.email == email
    assert saved_user.check_password(password)  # Проверяем хэшированный пароль


#Написать автотест, который проверит возникновение исключения при попытке обратиться к несуществующей записи в БД
@pytest.mark.django_db
def test_user_does_not_exist_exception():
    nonexistent_username = "nonexist"
    
    
    with pytest.raises(ObjectDoesNotExist, match="User matching query does not exist."):
        User.objects.get(username=nonexistent_username)