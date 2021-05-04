from typing import ByteString
import json

from fastapi import FastAPI, File, UploadFile

from .utils import similarity_service, get_speaker_duration

with open('/app/resources/config.json') as f:
    config = json.load(f)

app = FastAPI()


@app.post("/similarity_service")
async def similarity_service_(
        wav_content: UploadFile = File(...),
        embedding: str = ''
):
    wav_content = await wav_content.read()
    embedding = embedding.encode()
    result = similarity_service(
        wav_content=wav_content,
        embedding=embedding,
        speaker_index_path=config['speaker_index_path'],
        speaker_database_path=config['speaker_database_path'],
        wav_base_folder=config['wav_base_folder'],
        embedding_size=config['embedding_size'],
        max_speaker_duration=config['max_speaker_duration'],
        similarity_threshold=config['similarity_threshold']
)
    return result


@app.post("/speaker_duration")
async def speaker_duration_(
        embedding: str = '',
        similarity_threshold: float = -10.
):
    embedding = embedding.encode()
    if similarity_threshold < -1:
        similarity_threshold = config['similarity_threshold']
    duration = get_speaker_duration(
        embedding=embedding,
        speaker_index_path=config['speaker_index_path'],
        speaker_database_path=config['speaker_database_path'],
        embedding_size=config['embedding_size'],
        max_speaker_duration=config['max_speaker_duration'],
        similarity_threshold=similarity_threshold
)
    return {'embedding': embedding, 'duration': duration}
