import os
import sys

import pytest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import app, equipment


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_equipment():
    equipment.clear()

    equipment.extend([
        {
            "asset_id": "LAB001",
            "name": "Cisco Router",
            "category": "Networking",
            "status": "Available"
        },
        {
            "asset_id": "LAB002",
            "name": "Digital Oscilloscope",
            "category": "Electronics",
            "status": "Issued"
        },
        {
            "asset_id": "LAB003",
            "name": "Arduino Uno",
            "category": "Electronics",
            "status": "Maintenance"
        }
    ])

    yield


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_equipment_api(client):
    response = client.get("/api/equipment")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 3
    assert data[0]["asset_id"] == "LAB001"


def test_add_valid_equipment(client):
    response = client.post(
        "/add",
        data={
            "asset_id": "LAB004",
            "name": "Network Switch",
            "category": "Networking"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    assert any(
        item["asset_id"] == "LAB004"
        for item in equipment
    )


def test_reject_invalid_asset_id(client):
    response = client.post(
        "/add",
        data={
            "asset_id": "INVALID",
            "name": "Test Equipment",
            "category": "Other"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    assert not any(
        item["asset_id"] == "INVALID"
        for item in equipment
    )


def test_reject_duplicate_asset_id(client):
    original_count = len(equipment)

    response = client.post(
        "/add",
        data={
            "asset_id": "LAB001",
            "name": "Another Router",
            "category": "Networking"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert len(equipment) == original_count