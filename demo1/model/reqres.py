__all__ = ['ReqRes']

from sqlalchemy import Column, Integer, String

from base import Base, engine


class ReqRes(Base):
    __tablename__ = 'ReqRes'
    id = Column(Integer, primary_key=True)
    req_ts = Column(String, unique=False, nullable=False)
    req_method = Column(String, unique=False, nullable=False)
    req_path = Column(String, unique=False, nullable=False)
    req_headers = Column(String, unique=False, nullable=True)
    req_payload = Column(String, unique=False, nullable=True)
    res_ts = Column(String, unique=False, nullable=False)
    res_status = Column(Integer, unique=False, nullable=False)
    res_content_type = Column(String, unique=False, nullable=False)
    res_payload = Column(String, unique=False, nullable=True)

Base.metadata.create_all(bind=engine)