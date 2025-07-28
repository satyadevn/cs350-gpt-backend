from    pydantic        import  BaseModel

class QueryRequest ( BaseModel ):
    user_id                      : str
    query_text                   : str

class QueryResponse( BaseModel ) :
    response_text                : str
    input_tokens                 : int
    output_tokens                : int 
