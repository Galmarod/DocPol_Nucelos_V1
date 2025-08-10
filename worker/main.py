# worker/main.py
from fastapi import FastAPI, Request
from worker.processor import handle_task

app = FastAPI()

@app.post("/task")
async def process_task(request: Request):
    payload = await request.json()
    result = handle_task(payload)
    return {"status": "ok", "result": result}

@app.get("/")
async def root():
    return {"message": "Worker activo"}
