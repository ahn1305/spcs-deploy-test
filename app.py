from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/process")
def process_data(name: str):
    return {"message": f"Hello {name}, processed in SPCS!"}
