import os
from sqlalchemy import create_engine, Column, Integer, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = os.getenv("DATABASE_URI", "")

if DATABASE_URI == "":
    print("Can't find DATABASE_URI from env")
    exit(1)

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class GdeltRaw(Base):
    __tablename__ = 'gdelt_raw'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}

    id = Column('ID', Integer, primary_key=True)
    record_id = Column('RECORDID', String(20), index=True, unique=True)
    date = Column('DATE', Integer)
    numarts = Column('NUMARTS', Integer)
    counts = Column('COUNTS', Text)
    themes = Column('THEMES', Text)
    locations = Column('LOCATIONS', Text)
    persons = Column('PERSONS', Text)
    organizations = Column('ORGANIZATIONS', Text)
    tone = Column('TONE', Text)
    cameoeventids = Column('CAMEOEVENTIDS', Text)
    sources = Column('SOURCES', Text)
    sourceurls = Column('SOURCEURLS', Text)


Base.metadata.create_all(engine)
