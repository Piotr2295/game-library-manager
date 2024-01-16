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
