from enum import Enum

import structlog
from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from redis.exceptions import ConnectionError
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlmodel import Session

from boffin.config import get_settings

router = APIRouter(prefix="/status", tags=["status"])

logger = structlog.get_logger()


class ServiceStatus(str, Enum):
    OK = "OK"
    ERROR = "Error"


class ApplicationHealth(BaseModel):
    database: ServiceStatus
    redis: ServiceStatus

    def overall_status(self) -> ServiceStatus:
        services = (getattr(self, f) for f in self.model_fields.keys())

        if all(s == ServiceStatus.OK for s in services):
            return ServiceStatus.OK

        return ServiceStatus.ERROR


@router.get(
    "/healthcheck",
    responses={
        200: {
            "model": ApplicationHealth,
            "description": "Application is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "database": ServiceStatus.OK,
                        "redis": ServiceStatus.OK,
                    }
                }
            },
        },
        503: {
            "model": ApplicationHealth,
            "description": (
                "Something is wrong with the application. If any of the services are "
                "unavailable, the application will return a 503 status code."
            ),
            "content": {
                "application/json": {
                    "example": {
                        "database": ServiceStatus.ERROR,
                        "redis": ServiceStatus.OK,
                    }
                }
            },
        },
    },
)
async def check_application_health(
    response: Response,
) -> ApplicationHealth:
    # Initialize the health status
    health = ApplicationHealth(
        database=ServiceStatus.ERROR,
        redis=ServiceStatus.ERROR,
    )

    # Check the database connection
    try:
        session = Session(get_settings().database_engine)
        session.exec(select(1)).one()  # type: ignore
    except OperationalError:
        health.database = ServiceStatus.ERROR
    else:
        health.database = ServiceStatus.OK
    finally:
        session.close()

    # Check the Redis connection
    try:
        await get_settings().redis_client.ping()
    except ConnectionError:
        health.redis = ServiceStatus.ERROR
    else:
        health.redis = ServiceStatus.OK

    # Set the response code based on overall application health
    if health.overall_status() == ServiceStatus.OK:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return health
