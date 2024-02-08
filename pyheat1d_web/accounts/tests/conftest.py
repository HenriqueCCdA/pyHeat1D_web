import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from model_bakery import baker

User = get_user_model()

fake = Faker()


@pytest.fixture
def user(db):
    return baker.make(User)


@pytest.fixture
def user_with_password(db):
    password = fake.password()
    user = User.objects.create(email=fake.email(), password=password)
    user.plain_password = password
    return user


@pytest.fixture
def user_logged(client, user_with_password):
    client.force_login(user_with_password)
    return user_with_password


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(email=fake.email(), password=fake.password())
