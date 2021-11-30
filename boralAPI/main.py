import uvicorn
from fastapi import FastAPI
from Api.config import Config, Development, Production
from Api.controller.beweries import beweries_router
from Api.controller.order import order_router
from Api.controller.token import token_router


def registerRoutes(app:FastAPI)->None:
    app.include_router(token_router)
    app.include_router(order_router)
    app.include_router(beweries_router)


def main():
    if Config.API_ENV == "devel":
        app = FastAPI(
                debug=Development.DEBUG,
                title=Development.API_TITLE,
                description=Development.API_DESCRIPTION,
                docs_url=Development.API_DOCS_URL,
                version=Development.API_VERSION,
            )
    else:
        app = FastAPI(
                debug=Production.DEBUG,
                title=Production.API_TITLE,
                description=Production.API_DESCRIPTION,
                docs_url=Production.API_DOCS_URL,
                version=Production.API_VERSION,
            )

    registerRoutes(app)
    # http://127.0.0.1:8000/docs
    return app


if __name__ == "__main__":
    app = main()
    uvicorn.run(app, host="127.0.0.1", port=8000)