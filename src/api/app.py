from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from src.core.agent import PreprocessingAgent
from src.models.domain import EmbedRequest, SearchRequest, SearchResponse
from src.config import settings
from src.logger import configure_logging

configure_logging()
app = FastAPI(title="Song Preprocessor API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, include_in_schema=False)
agent = PreprocessingAgent()

@app.post("/preprocess/", response_model=dict)
async def preprocess(req: EmbedRequest):
    try:
        return await agent.preprocess_and_embed(req.track_id, req.clean_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/", response_model=SearchResponse)
def search(req: SearchRequest):
    try:
        return agent.search_similar(req.query_text, req.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))