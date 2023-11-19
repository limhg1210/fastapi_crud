from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session

from apps.exceptions import NotFoundError
from apps.item.models import Item


class ItemRepository:
    def __init__(
            self,
            session: async_scoped_session,
            cache: Redis,
            model: Item,
    ):
        self.session = session
        self.cache = cache
        self.model = model

    async def get_by_id(self, item_id: int) -> Item:
        cache_item = await self.get_by_id_from_cache(item_id)
        if cache_item:
            return cache_item

        item = await self.get_by_id_from_db(item_id)
        await self._set_cache(item)

        return item

    async def get_by_id_from_cache(self, item_id: int) -> Item | None:
        item_json = await self.cache.get(f"item_{item_id}")
        if item_json:
            return Item.from_json(item_json)

    async def get_by_id_from_db(self, item_id: int) -> Item:
        async with self.session() as db:
            item: Item = (await db.scalars(select(self.model).where(self.model.id == item_id))).first()

        if not item:
            raise NotFoundError

        return item

    async def save(self, item: Item) -> Item:
        async with self.session() as db:
            db.add(item)
            await db.commit()
            await db.refresh(item)

        await self._delete_cache(item.id)
        return item

    async def delete(self, item: Item) -> None:
        async with self.session() as db:
            await db.delete(item)
            await db.commit()

        await self._delete_cache(item.id)

    async def _set_cache(self, item: Item) -> None:
        await self.cache.set(f"item_{item.id}", item.to_json())

    async def _delete_cache(self, item_id: int) -> None:
        await self.cache.delete(f"item_{item_id}")
