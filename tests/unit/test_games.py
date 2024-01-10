import os
import sys

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from app.main import app
from app.internal.database import get_db
from app.routers.games import create_game

client = TestClient(app)


@pytest.fixture
def mock_db():
    return Mock()


@pytest.fixture
def mock_game_service():
    return Mock()


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to your game library!"}


def test_get_games():
    response = client.get("/games/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_game_invalid_id(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.get("/games/999")

    assert response.status_code == 404


# def test_create_game_success(mock_db, mock_game_service):
#     mock_game_service.create_game.return_value = {
#         "id": 99,
#         "title": "Test Game",
#         "platform": "PS5",
#         "genre": "FPS",
#         "cover_image": "link1",
#         "screenshots": "link2",
#         "video_links": "link3"
#     }
#
#     app.dependency_overrides[get_db] = lambda: mock_db
#     app.dependency_overrides[create_game] = lambda: mock_game_service
#
#     response = client.post(
#         "/games/",
#         json=
#         {
#             "id": 99,
#             "title": "Test Game",
#             "platform": "PS5",
#             "genre": "FPS",
#             "cover_image": "link1",
#             "screenshots": "link2",
#             "video_links": "link3"
#         }
#     )
#
#     print(response.text)
#     assert response.status_code == 201
#     assert response.json()["title"] == "Test Game"
#
#     mock_game_service.create_game.assert_called_once()
#

# def test_get_game_success(mock_db):
#     expected_game =
#     {
#             "id": 1,
#             "title": "Test Game",
#             "platform": "PS5",
#             "genre": "FPS",
#             "cover_image": "link1",
#             "screenshots": "link2",
#             "video_links": "link3"
#         }
#
#     mock_db.query.return_value.filter.return_value.first.return_value = expected_game
#
#     response = client.get("/games/1")
#
#     assert response.status_code == 200
#     assert response.json() == expected_game
#