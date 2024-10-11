from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData
from sqlalchemy.ext.declarative import declarative_base
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column

metadata = MetaData()

# operation = Table(
#     "operation", 
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("quantity", String),
#     Column("figi", String),
#     Column("instrument_type", String, nullable=True),
#     Column("data", TIMESTAMP),
#     Column("type", String)

# )


class Operation(Base):
    __tablename__ = "operation"
    id: Mapped[int] =  mapped_column(primary_key=True)
    quantity: Mapped[str]
    figi: Mapped[str]
    instrument_type: Mapped[int] = mapped_column(nullable=True)
    # data: Mapped[str] = Column(TIMESTAMP)
    data: Mapped[str] = mapped_column(TIMESTAMP)
    type:Mapped[str] 


