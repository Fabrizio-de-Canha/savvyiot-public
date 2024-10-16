from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

pg_url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SERVER')}/savvyiot"
pg_url_socket = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SERVER')}/savvyiot"

pg_engine = create_engine(
    pg_url,
    echo=False,
)

session_maker = sessionmaker(
    pg_engine, expire_on_commit=False
)

Base = declarative_base()