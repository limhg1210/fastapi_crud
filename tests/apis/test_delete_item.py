import pytest
from sqlalchemy import select

from apps.item.models import Item


@pytest.mark.asyncio
async def test_delete_item_response_200(test_client, session_factory):
    # Given
    item = Item(name="test_name", content="test_content")

    with session_factory() as db:
        db.add(item)
        db.commit()
        db.refresh(item)

    # When
    response = await test_client.delete(f"/item/{item.id}")

    # Then
    assert response.status_code == 200

    with session_factory() as db:
        item = (db.scalars(select(Item).where(Item.id == item.id))).first()

    assert item is None


@pytest.mark.asyncio
async def test_delete_item_response_404(test_client):
    # When
    response = await test_client.get("/item/0")

    # Then
    assert response.status_code == 404
