from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection configuration
DB_URL = "mysql+mysqlconnector://root:root@localhost:3306/microdata"

engine = create_engine(DB_URL)
LocalSession = sessionmaker(bind=engine)
Base = declarative_base()   

TABLE_NAME = "microdata_op"
STATE_TABLE_NAME = "codes"