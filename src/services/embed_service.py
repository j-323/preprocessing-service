from pymilvus import connections, Collection
from src.models.domain import EmbedRequest, EmbedResponse
from src.config import settings
from src.core.exceptions import ServiceError

class EmbedService:
    def __init__(self, collection_name: str = "songs"):
        connections.connect(host=settings.milvus_host, port=str(settings.milvus_port))
        self.collection = Collection(collection_name)

    def embed(self, req: EmbedRequest) -> EmbedResponse:
        try:
            vector = req.metadata.pop("embedding")
            ent = {"track_id": req.track_id, "embedding": vector, "metadata": req.metadata}
            res = self.collection.insert([ent])
            return EmbedResponse(status="ok", milvus_id=res.primary_keys[0])
        except Exception as e:
            raise ServiceError(f"EmbedService failed: {e}")