import pytest
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()

fake = Faker()


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(email=fake.email(), password=fake.password())
