from	sqlalchemy	import		Column, Integer, String, DateTime, Text, ForeignKey
from	sqlalchemy.orm	import		relationship
from	datetime	import		datetime
from	db		import		Base

class QueryLog(Base):
    __tablename__ =       "queryLogs"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(String, index=True)
    query_text    = Column(String)
    response_text = Column(String)
    input_tokens  = Column(Integer)
    output_tokens = Column(Integer)
    timestamp     = Column(DateTime, default=datetime.utcnow)

class User ( Base ) :
    __tablename__ =       "users"
    id            =       Column ( Integer, primary_key=True, index=True )
    iitk_uid      =       Column ( String, unique=True, index=True )
    queries       =       relationship ( "Query", back_populates = "User" )

class Query ( Base ) :
    __tablename__ =       "queries"
    id            =       Column ( Integer, primary_key=True, index=True )
    user_id       =       Column ( Integer, ForeignKey ( "users.id" ) )
    query_text    =       Column ( Text )
    response_text =       Column ( Text )
    timestamp     =       Column ( DateTime, default=datetime.utcnow ) 

    user          =       relationship ( "User", back_populates = "queries" )
    
