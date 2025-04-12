import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from law_service import LawService
from utils import Output

law_service = LawService()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    law_service.start()
    yield
    law_service.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/query", response_model=Output)
async def root(query: str):
    return law_service.query(query)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
