from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

DATABASE_URL = config["PSQL"]["DATABASE_URL"]
DATABASE = config["PSQL"]["DATABASE"]
USER = config["PSQL"]["USER"]
PASSWORD = config["PSQL"]["PASSWORD"]

DATABASE_URL = DATABASE_URL.format(DATABASE, USER, PASSWORD)

_engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

Base = declarative_base()
