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
def superuser(db):
    return User.objects.create_superuser(email=fake.email(), password=fake.password())
