from unittest.mock import Mock


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
