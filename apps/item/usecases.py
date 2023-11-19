from apps.item.models import Item
from apps.item.repositories import ItemRepository
from apps.item.schemas import ItemCreate, ItemUpdate


class ItemUsecase:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    async def read_item(self, item_id: int) -> Item:
        item = await self.item_repository.get_by_id(item_id)
        return item

    async def create_item(self, schema: ItemCreate) -> Item:
        item = Item.create(schema)
        await self.item_repository.save(item)
        return item

    async def update_item(self, item_id: int, schema: ItemUpdate) -> Item:
        item = await self.item_repository.get_by_id_from_db(item_id)
        item.update(schema)
        await self.item_repository.save(item)
        return item

    async def delete_item(self, item_id: int) -> None:
        item = await self.item_repository.get_by_id_from_db(item_id)
        await self.item_repository.delete(item)
