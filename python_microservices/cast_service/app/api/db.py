import os

from dotenv import load_dotenv
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine)

from databases import Database

load_dotenv()
DATABASE_URL = os.getenv("CAST_DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

casts = Table(
    'casts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('nationality', String(20)),
)

database = Database(DATABASE_URL)
