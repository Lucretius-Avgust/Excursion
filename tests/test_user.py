import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        # без отчества
        {
            "first_name": "Test",
            "last_name": "User",
            "email": "test1@example.com",
            "password": "12345678"
        },
        # с отчеством
        {
            "first_name": "Test",
            "last_name": "User",
            "middle_name": "Ivanovich",
            "email": "test2@example.com",
            "password": "12345678"
        },
    ]
)
async def test_create_user_valid_data(client, payload):
    response = await client.post("/user/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]

    # проверяем отчество только если оно было передано
    if "middle_name" in payload:
        assert data["middle_name"] == payload["middle_name"]
    else:
        assert "middle_name" not in data or data["middle_name"] is None



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,expected_status",
    [
        # неверный email
        ({"first_name": "Test", "last_name": "User", "email": "not-an-email", "password": "12345678"}, 422),
        # слишком короткий пароль
        ({"first_name": "Test", "last_name": "User", "email": "short@example.com", "password": "123"}, 422),
        # отсутствует email
        ({"first_name": "Test", "last_name": "User", "password": "12345678"}, 422),
        # отсутствует пароль
        ({"first_name": "Test", "last_name": "User", "email": "nopass@example.com"}, 422),
        # пустой JSON
        ({}, 422),
    ]
)
async def test_create_user_invalid_data(client, payload, expected_status):
    response = await client.post("/user/", json=payload)
    assert response.status_code == expected_status


