from contextlib import contextmanager
from os import getenv
from typing import Generator

from sqlalchemy import create_engine
from sqlmodel import Session

ENGINE = create_engine(getenv("DATABASE_URL", ""))


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
