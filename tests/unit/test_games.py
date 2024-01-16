import os
import sys

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.internal.models import Game
from tests.unit.utils import MockDb

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from app.main import app
from app.internal.database import get_db

client = TestClient(app)


@pytest.fixture
def mock_db():
    mock = MockDb()
    return mock


@pytest.fixture
def mock_game_service():
    mock = Mock(name='game_service_mock')
    return mock


@pytest.fixture
def example_game_from_db():
    game_object_from_db = Game(
        title="Test Game",
        platform="PS5",
        genre="FPS",
        cover_image="link1",
        screenshots="link2",
        video_links="link3"
    )
    return game_object_from_db


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to your game library!"}


def test_get_games():
    response = client.get("/games/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_game_invalid_id(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get("/games/999")

    assert response.status_code == 404


def test_create_game_success(mock_db, mock_game_service):
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.post(
        "/games/",
        json=
        {
            "id": 1,
            "title": "Test Game",
            "platform": "PS5",
            "genre": "FPS",
            "cover_image": "link1",
            "screenshots": "link2",
            "video_links": "link3"
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Game"


def test_create_game_unsuccessful(mock_db, mock_game_service, example_game_from_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    mock_db.first = Mock(return_value=example_game_from_db)
    response = client.post(
        "/games/",
        json=
        {
            "id": 1,
            "title": "Test Game2",
            "platform": "PS5",
            "genre": "FPS",
            "cover_image": "link1",
            "screenshots": "link2",
            "video_links": "link3"
        }
    )
    assert response.status_code == 400
    assert response.text == '{"detail":"Game already exists"}'
