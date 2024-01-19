import os
import sys

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock

from starlette import status

from app.internal.models import Game
from app.routers.auth import get_current_active_user
from tests.unit.utils import MockDb, MockUser

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
def mock_current_user():
    mock = MockUser()
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


@pytest.fixture
def example_game_from_db2():
    game_object_from_db = Game(
        id=1,
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


def test_create_game_success(mock_db):
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


def test_create_game_unsuccessful(mock_db, example_game_from_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    mock_db.first = Mock(return_value=example_game_from_db)
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
    assert response.status_code == 400
    assert response.text == '{"detail":"Game already exists"}'


def test_update_game(mock_db, example_game_from_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    mock_db.first = Mock(return_value=example_game_from_db)
    response = client.put(
        "/games/1",
        json=
        {
            "id": 1,
            "title": "Test Game2",
            "platform": "PS4",
            "genre": "FPS",
            "cover_image": "new_link",
            "screenshots": "link2",
            "video_links": "link3"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Game2"


def test_update_game_game_not_found(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.put(
        "/games/1",
        json=
        {
            "id": 1,
            "title": "Test Game2",
            "platform": "PS4",
            "genre": "FPS",
            "cover_image": "new_link",
            "screenshots": "link2",
            "video_links": "link3"
        }
    )
    assert response.status_code == 404
    assert response.text == '{"detail":"Game not found"}'


def test_delete_game(mock_db, mock_current_user, example_game_from_db2):
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
    mock_db.first = Mock(return_value=example_game_from_db2)
    response = client.delete(
        "/games/1"
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Game"


def test_delete_game_unauthorized(mock_db, example_game_from_db2):
    app.dependency_overrides[get_db] = lambda: mock_db
    mock_db.first = Mock(return_value=example_game_from_db2)
    response = client.delete(
        "/games/1"
    )
    assert response.status_code == 401
    assert response.text == '{"detail":"Not authenticated"}'


def test_delete_game_game_not_found(mock_db, mock_current_user, example_game_from_db2):
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
    response = client.delete(
        "/games/1"
    )
    assert response.status_code == 404
    assert response.text == '{"detail":"Game not found"}'


# def test_delete_game_inactive_user(mock_db, mock_current_user, example_game_from_db2):
#     app.dependency_overrides[get_db] = lambda: mock_db
#     app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
#     mock_db.first = Mock(return_value=example_game_from_db2)
#     mock_current_user = Mock(side_effect=HTTPException(status_code=400, detail="Inactive user"))
#     response = client.delete(
#         "/games/1"
#     )
#     assert response.status_code == 400
#     assert response.text == '{"detail":"Inactive user"}'
