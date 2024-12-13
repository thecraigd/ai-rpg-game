from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/test")
async def read_root():
    return {"message": "Hello from FastAPI!"}

handler = Mangum(app)