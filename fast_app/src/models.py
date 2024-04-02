from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, func


metadata = MetaData()

process = Table(
    'process',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('pid', Integer, nullable=False),
    Column('status', String, nullable=False, server_default='running'),
    Column('start_number', Integer, server_default=str(0), nullable=False),
    Column('begin_date', DateTime(timezone=True), server_default=func.now()),
    Column('finish_date', DateTime(timezone=True)),
)


