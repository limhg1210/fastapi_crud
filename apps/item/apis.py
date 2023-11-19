from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from apps.di_container import Container
from apps.item.repositories import ItemRepository
from apps.item.schemas import ItemRead, ItemCreate, ItemUpdate
from apps.item.usecases import ItemUsecase


router = APIRouter()


@router.get("/item/{item_id}", response_model=ItemRead)
@inject
async def read_item(
        item_id: int,
        item_usecase: ItemUsecase = Depends(Provide[Container.item_usecase]),
):
    item = await item_usecase.read_item(item_id)
    return item


@router.post("/item/", response_model=ItemRead)
@inject
async def create_item(
        schema: ItemCreate,
        item_usecase: ItemUsecase = Depends(Provide[Container.item_usecase]),
):
    item = await item_usecase.create_item(schema)
    return item


@router.put("/item/{item_id}", response_model=ItemRead)
@inject
async def update_item(
        item_id: int,
        schema: ItemUpdate,
        item_usecase: ItemUsecase = Depends(Provide[Container.item_usecase]),
):
    item = await item_usecase.update_item(item_id=item_id, schema=schema)
    return item


@router.delete("/item/{item_id}")
@inject
async def delete_item(
        item_id: int,
        item_usecase: ItemUsecase = Depends(Provide[Container.item_usecase]),
):
    await item_usecase.delete_item(item_id)
