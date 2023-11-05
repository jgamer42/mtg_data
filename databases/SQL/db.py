import os
from dotenv import load_dotenv
load_dotenv() 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


model_base = declarative_base()
engine = create_engine(f"postgresql+psycopg2://{os.environ['PROJECT_DB_USER']}:{os.environ['PROJECT_DB_PASSWORD']}@{os.environ['PROJECT_DB_HOST']}/{os.environ['PROJECT_DB_NAME']}")
Session = sessionmaker(bind=engine)
session = Session()
