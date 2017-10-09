from django.contrib.auth import get_user_model
from faker import Factory

fake = Factory.create()


def a_user():
    return get_user_model().objects.create(
        email=fake.email(),
        username=fake.user_name(),
    )
