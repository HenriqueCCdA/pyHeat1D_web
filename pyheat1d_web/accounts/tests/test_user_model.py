import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.unit
def test_positive_create_user(user):
    assert user.pk
    assert User.objects.exists()


@pytest.mark.unit
def test_positive_create_superuser(superuser):
    assert superuser.is_staff
    assert superuser.is_superuser


@pytest.mark.unit
def test_positive_default(user):
    assert not user.is_staff
    assert user.is_active
    assert not user.is_superuser


@pytest.mark.unit
def test_str(user):
    assert str(user) == user.email


@pytest.mark.unit
def test_normilized_email(db):
    user = User(email="lunadonald@EXAMPLE.oRg")
    user.clean()
    assert user.email == "lunadonald@example.org"
