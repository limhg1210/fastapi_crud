from dependency_injector import containers, providers
from redis.asyncio import Redis

from apps.item.models import Item
from apps.item.repositories import ItemRepository
from apps.item.usecases import ItemUsecase
from config.database import Database
from config.settings import get_settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".item.apis"])
    config = providers.Configuration()

    cache = providers.Singleton(
        Redis,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        decode_responses=True,
    )
    database = providers.Singleton(
        Database,
        url=config.DATABASE_URL,
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


def create_container(env_name: str = "default"):
    container = Container()
    container.config.from_dict(get_settings(env_name=env_name).model_dump())

    return container
