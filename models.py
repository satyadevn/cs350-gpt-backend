from	sqlalchemy	import		Column, Integer, String, DateTime, Text, ForeignKey
from	sqlalchemy.orm	import		relationship
from	datetime	import		datetime
from	db		import		Base

#==============================================================
# This contains all the database models for storing a log of all
# the queries. 
#==============================================================
class QueryLog(Base):
    __tablename__ =       "queryLogs"
    id            = Column(Integer, primary_key=True, index=True)
    query_text    = Column(String)
    response_text = Column(String)
    input_tokens  = Column(Integer)
    output_tokens = Column(Integer)
    timestamp     = Column(DateTime, default=datetime.utcnow)

    
