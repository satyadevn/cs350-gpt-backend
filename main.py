from    fastapi         import FastAPI, Depends
#from    fastapi.middleware.cors import CORSMiddleware
#from    sqlalchemy.orm  import Session
#from    db              import SessionLocal, Base, engine
#import  models, schemas
import  schemas
from    dotenv          import load_dotenv
import  os
from    openai          import OpenAI
from    rag             import get_relevant_chunks
import  requests        as      req

# Load env vars and set up OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#GOOGLE_CAPTCHA_SECRET = os.getenv("GOOGLE_CAPTCHA_SECRET")
# Create tables
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# prevent queries other than through the front end. You may disable this
# for local tests.
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://cs350-gpt-frontend.onrender.com"],
#     allow_methods=["POST"],
#     allow_headers=["*"]
# )

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# /query endpoint
@app.post("/query", response_model=schemas.QueryResponse)



def handle_query(payload: schemas.QueryRequest): # db: Session = Depends(get_db)):

    retrieved = get_relevant_chunks ( payload.query_text )
    context   = "\n\n".join ( retrieved )
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages = [
            { "role" : "user",
              "content" :
              "Use the following lecture material to answer the question." },
            { "role" : "system", "content" : context },
            { "role" : "user", "content" : payload.query_text }],
        max_tokens=500
    )

    output_text = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    # db.add(models.QueryLog(
    #     query_text=payload.query_text,
    #     response_text=output_text,
    #     input_tokens=input_tokens,
    #     output_tokens=output_tokens,
    # ))
    # db.commit()

    return schemas.QueryResponse(
        response_text=output_text,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
