from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from apps.di_container import create_container
from apps.exceptions import NotFoundError
from apps.item.apis import router as item_router


def create_app(env_name: str = "default"):
    _app = FastAPI()
    _app.container = create_container(env_name=env_name)
    _app.include_router(item_router)

    @_app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"message": "Not Found Error"},
        )

    return _app


app = create_app()
