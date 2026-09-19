from fastapi import FastAPI


FOUNDATION_STATUS = {
    "application": "ViDAP",
    "scope": "phase-0-foundation",
    "status": "ready",
}


def create_app() -> FastAPI:
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

    @app.get("/api/status")
    async def foundation_status() -> dict[str, str]:
        return FOUNDATION_STATUS

    return app
