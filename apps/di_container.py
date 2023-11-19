from dependency_injector import containers, providers
from redis.asyncio import Redis

from apps.item.models import Item
from apps.item.repositories import ItemRepository
from apps.item.usecases import ItemUsecase
from config.database import Database
from config.settings import get_settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".item.apis"])
    settings = get_settings()

    cache = providers.Singleton(
        Redis,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )
    database = providers.Singleton(
        Database,
        url=(
            f"mysql+aiomysql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
            f"@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}"
        )
    )

    # repositories
    item_repository = providers.Singleton(
        ItemRepository,
        session=database.provided.session_factory,
        cache=cache,
        model=Item,
    )

    # usecases
    item_usecase = providers.Singleton(
        ItemUsecase,
        item_repository=item_repository,
    )


container = Container()
