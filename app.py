from fastapi import FastAPI
from service.service import service_impl
import uvicorn

app = FastAPI(
    title="Personalized landing page",
    description="Personalized landing page",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "Personalized landing page服务已运行！"}


@app.post("/personalize")
def personalize(playbook:dict):
    service_impl.gen_personalized_page(playbook)
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)