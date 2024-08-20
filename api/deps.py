from db.session import session_maker, Base, pg_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends, HTTPException

def connect() -> None:
    with pg_engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all, checkfirst=True)

def disconnect() -> None:
    if pg_engine:
        pg_engine.dispose()

def get_session() -> Session: # type: ignore
    with session_maker() as session:
        try:
            yield session
            session.commit()
        except SQLAlchemyError as sql_ex:
            session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            session.rollback()
            raise http_ex
        finally:
            session.close()