from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)
    congress = Column(Integer)
    latest_action_date = Column(Date)
    action_text = Column(String)
    bill_num = Column(Integer)
    origin_chamber = Column(String)
    origin_chamber_code = Column(String)
    bill_type = Column(String)
    last_update_date = Column(Date)
    url = Column(String)


