from typing import ByteString
import json

from fastapi import FastAPI, File, UploadFile

from .utils import indexer

with open('/app/resources/config.json') as f:
    config = json.load(f)

app = FastAPI()


@app.post("/similarity_service")
async def create_upload_file(
        wav_content: UploadFile = File(...),
        embedding: str = ''
):
    wav_content = await wav_content.read()
    embedding = embedding.encode()
    result = indexer(
        wav_content,
        embedding,
        speaker_index_path=config['speaker_index_path'],
        speaker_database_path=config['speaker_database_path'],
        wav_base_folder=config['wav_base_folder'],
        embedding_size=config['embedding_size'],
        speaker_duration=config['speaker_duration'],
        similarity_threshold=config['similarity_threshold']
)
    return result
