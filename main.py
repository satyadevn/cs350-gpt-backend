from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal, Base, engine
import models, schemas
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load env vars and set up OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# /query endpoint
@app.post("/query", response_model=schemas.QueryResponse)



def handle_query(payload: schemas.QueryRequest, db: Session = Depends(get_db)):
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": payload.query_text}],
        max_tokens=100
    )

    output_text = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    db.add(models.QueryLog(
        user_id=payload.user_id,
        query_text=payload.query_text,
        response_text=output_text,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    ))
    db.commit()

    return schemas.QueryResponse(
        response_text=output_text,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
