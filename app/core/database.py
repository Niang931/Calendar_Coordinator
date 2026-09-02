from app.core.config import setting
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.logger import logger
from sqlalchemy import exc


DATABASE_URL = setting.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,
                            autocommit=False,
                            bind=engine)


def get_session():
    session = None
    try:
        session = SessionLocal()
        yield session
        session.commit()
    except exc.SQLAlchemyError as e:
        logger.error(e)
        if session:
            session.rollback()
        raise
    finally:
        if session is not None:
            session.close()
        
     


