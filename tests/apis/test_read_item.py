import pytest

from apps.item.models import Item


@pytest.mark.asyncio
async def test_read_item_response_200(test_client, session_factory):
    # Given
    item = Item(name="test_name", content="test_content")

    with session_factory() as db:
        db.add(item)
        db.commit()
        db.refresh(item)

    # When
    response = await test_client.get(f"/item/{item.id}")

    # Then
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["id"] == item.id
    assert response_json["created"] == item.created.isoformat()
    assert response_json["name"] == item.name
    assert response_json["content"] == item.content


@pytest.mark.asyncio
async def test_read_item_response_404(test_client):
    # When
    response = await test_client.get("/item/0")

    # Then
    assert response.status_code == 404
