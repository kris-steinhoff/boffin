import uuid
from http import HTTPStatus

import strawberry
import structlog
from colorama import Back, Fore, Style
from fastapi import FastAPI, Request, Response
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

from boffin.config import get_settings
from boffin.status.rest import router as status_router
from boffin.student.graphql import StudentMutation, StudentQuery, StudentSubscription
from boffin.student.rest import router as student_router

logger = structlog.get_logger()

app = FastAPI(
    title="Boffin",
    description="[GraphQL](/graphql)",
)
app.include_router(student_router)
app.include_router(status_router)


Query = merge_types(
    "Query",
    (StudentQuery,),
)
Mutation = merge_types(
    "Mutation",
    (StudentMutation,),
)
Subscription = merge_types(
    "Subscription",
    (StudentSubscription,),
)
schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
graphql_app: GraphQLRouter = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql", include_in_schema=False)


async def log_access(request: Request, response: Response) -> None:
    if not any(
        (
            get_settings().access_log,
            get_settings().dev_mode,
            request.url.path != "/status/healthcheck",
        )
    ):
        return

    status_color = Fore.RESET

    if response.status_code >= 200:
        status_color = Fore.GREEN
    if response.status_code >= 300:
        status_color = Fore.CYAN
    if response.status_code >= 400:
        status_color = Fore.RED
    if response.status_code >= 500:
        status_color = Style.BRIGHT + Back.RED

    access = (
        f'{Style.BRIGHT}"{request.method.upper()} {request.url.path} '
        f'{request.scope.get("type", "").upper()}/{request.scope.get("http_version", "")}"{Style.RESET_ALL} '
        f"{status_color}{response.status_code} {HTTPStatus(response.status_code).phrase}{Style.RESET_ALL}"
    )

    logger.info(access, status_code=response.status_code)


@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    request_id = request.headers.get("request-id", uuid.uuid4().hex)

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
    )

    try:
        response: Response = await call_next(request)
    except Exception as exc:
        logger.exception(exc)
        response = Response(
            content="Internal Server Error",
            status_code=500,
        )
    finally:
        await log_access(request, response)

    return response


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "boffin.main:app",
        host=settings.server_host,
        port=settings.server_port,
        workers=settings.server_workers,
        reload=settings.dev_mode,
        access_log=False,
        use_colors=True,
    )
