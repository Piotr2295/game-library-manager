from unittest.mock import Mock

from internal.models import User


class MockDb(Mock):
    def query(self, _):
        return self

    def filter(self, _):
        return self

    def first(self):
        return None

    def add(self, model):
        model.id = 1


class MockUser(Mock):
    def get_current_user(self, _):
        return self

    def get_current_active_user(self, _):
        return self


class MockNotEnoughPermissionUser(Mock):
    def get_current_user(self, _):
        user_object_from_db = User(
            id=1,
            username="test_user",
            email="test@mail.com",
            hashed_password="hashed_password",
            scopes=["me"],
            disabled=False,
        )
        return user_object_from_db

    def get_current_active_user(self, _):
        return self
