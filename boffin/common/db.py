from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlmodel import Session

from boffin.config import get_settings

ENGINE = create_engine(get_settings().database_url)


@contextmanager
def atomic() -> Generator[Session, None, None]:
    try:
        session = Session(ENGINE)
        yield session
    except Exception:
        raise
    else:
        session.commit()
    finally:
        session.rollback()

    session.close()
