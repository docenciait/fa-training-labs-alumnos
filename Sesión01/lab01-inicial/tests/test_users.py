import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_users():
    async with AsyncClient(base_url="http://app:8000") as ac:
        response = await ac.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
