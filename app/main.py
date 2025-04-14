import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from law_service import LawService
from utils import Output

law_service = LawService()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await law_service.start()
    yield
    await law_service.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/api/query", response_model=Output)
async def api_query(query: str, top_k: int):
    return await law_service.query(query, top_k)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9001)
