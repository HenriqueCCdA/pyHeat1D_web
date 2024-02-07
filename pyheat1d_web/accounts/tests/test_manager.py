import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.unit
def test_create_normilized_email(db):
    user = User.objects.create(email="lunadonald@EXAMPLE.oRg")
    assert user.email == "lunadonald@example.org"


@pytest.mark.unit
def test_create_missing_email(db):
    with pytest.raises(ValueError, match="The given email username must be set"):
        User.objects.create()
