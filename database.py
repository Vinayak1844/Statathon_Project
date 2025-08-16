from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_URL = "mysql+mysqlconnector://root:Vinayak%401844@localhost:3306/statathon"

engine = create_engine(DB_URL)
LocalSession = sessionmaker(bind=engine)
Base = declarative_base()   

Tablename = "output"