from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
def db_create():
    engine = create_engine('sqlite:///demo1.db')
    return engine

class Data(Base):
    __tablename__ ='Data'

    id = Column('id', Integer, primary_key=True)
    time_stamp = Column('time_stamp', String, unique=False, nullable=False)
    source_address = Column('source_address', String, unique=False, nullable=False)
    destination_address = Column('destination_address', String, unique=False, nullable=False)
    method = Column('method', String, unique=False, nullable=False)
    destination_api = Column('destination_api', String, unique=False, nullable=False)
    payload = Column('payload', String, unique=False, nullable=False)
    
    def __init__(self,time_stamp,source_address,destination_address,method,destination_api,payload):

        self.time_stamp = time_stamp
        self.source_address = source_address
        self.destination_address = destination_address
        self.method = method
        self.destination_api = destination_api
        self.payload = payload

engine = db_create()
Base.metadata.create_all(bind=engine)