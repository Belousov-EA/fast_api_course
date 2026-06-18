import pytest


@pytest.mark.asyncio
async def test_mvp_flow_from_login_to_public_read(client, seeded_admin_user):
    login_response = await client.post(
        "/api/auth/login",
        json={
            "email": "admin@example.com",
            "password": "strongpassword123",
        },
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
