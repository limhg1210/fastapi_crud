from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from apps.di_container import container
from apps.exceptions import NotFoundError
from apps.item.apis import router as item_router


app = FastAPI()

app.container = container
app.include_router(item_router)


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": "Not Found Error"},
    )
