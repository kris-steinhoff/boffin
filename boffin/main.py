import uuid

import strawberry
import structlog
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


@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    request_id = request.headers.get("request-id", uuid.uuid4().hex)

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
    )

    response: Response = await call_next(request)

    if get_settings().dev_mode and request.url.path != "/status/healthcheck":
        logger.info(
            f"{request.method.upper()} {request.url.path} "
            f"{request.scope.get("type", "").upper()}/"
            f"{request.scope.get("http_version", "")} {response.status_code}"
        )
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
