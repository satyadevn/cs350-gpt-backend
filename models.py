from    sqlalchemy      import          Column, Integer, String, DateTime
from    datetime        import          datetime
from    db              import          Base

class QueryLog(Base):
    __tablename__       =       "queryLogs"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(String, index=True)
    query_text    = Column(String)
    response_text = Column(String)
    input_tokens  = Column(Integer)
    output_tokens = Column(Integer)
    timestamp     = Column(DateTime, default=datetime.utcnow)

    
