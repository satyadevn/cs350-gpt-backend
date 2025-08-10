from    pydantic        import  BaseModel

#=====================================================================
# these are the models for the queries and the responses for
# interacting with the backend using messages. They are *not* for the
# database, which stores all the actual queries, their responses, and
# keeps track of token usage. for that, see elsewhere.
# ======================================================================
class QueryRequest ( BaseModel ) :
    user_id      : str
    query_text   : str

class QueryResponse( BaseModel ) :
    response_text : str
    input_tokens  : int
    output_tokens : int 
