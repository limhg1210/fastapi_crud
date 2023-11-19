import pytest
from sqlalchemy import select

from apps.item.models import Item


@pytest.mark.asyncio
async def test_update_item_response_200(test_client, session_factory):
    # Given
    item = Item(name="test_name", content="test_content")

    with session_factory() as db:
        db.add(item)
        db.commit()
        db.refresh(item)

    payload = {"name": "update_name", "content": "update_content"}

    # When
    response = await test_client.put(f"/item/{item.id}", json=payload)

    # Then
    assert response.status_code == 200

    response_json = response.json()
    with session_factory() as db:
        item = (db.scalars(select(Item).where(Item.id == response_json["id"]))).first()

    assert response_json["id"] == item.id
    assert response_json["created"] == item.created.isoformat()
    assert response_json["name"] == "update_name"
    assert response_json["content"] == "update_content"


@pytest.mark.asyncio
@pytest.mark.parametrize("payload", [{"name": "test_name"}, {"content": "test_content"}])
async def test_update_item_response_422(test_client, session_factory, payload):
    # Given
    item = Item(name="test_name", content="test_content")

    with session_factory() as db:
        db.add(item)
        db.commit()
        db.refresh(item)

    # When
    response = await test_client.post("/item", json=payload)

    # Then
    assert response.status_code == 422
