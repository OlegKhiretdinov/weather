import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(f'postgresql://{DATABASE_URL}', echo=True)

Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
