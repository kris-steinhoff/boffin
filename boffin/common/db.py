from sqlmodel import Session

from boffin.config import get_settings


def get_session() -> Session:
    return Session(get_settings().database_engine)
