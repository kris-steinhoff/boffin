from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session

from boffin.config import get_settings


@contextmanager
def atomic() -> Generator[Session, None, None]:
    try:
        session = Session(get_settings().database_engine)
        yield session
    except Exception:
        raise
    else:
        session.commit()
    finally:
        session.rollback()

    session.close()
