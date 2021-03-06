import base64
import io
import os
import uuid

import numpy as np
import soundfile as sf

from .sqlite_interface import SingletonDB
from .faiss_interface import SingletonFaiss


def convert_to_np(embedding):
    embedding = np.frombuffer(base64.b64decode(embedding), dtype=np.float32)
    return embedding


def get_speaker_duration(
        embedding,
        speaker_index_path,
        speaker_database_path,
        embedding_size,
        max_speaker_duration,
        similarity_threshold
):
    singleton_faiss = SingletonFaiss(speaker_index_path, embedding_size)
    singleton_db = SingletonDB(speaker_database_path)

    embedding = convert_to_np(embedding)
    singleton_faiss = SingletonFaiss(speaker_index_path, embedding_size)
    similarities, indexes = singleton_faiss.search(embedding, max_speaker_duration)

    # filter embeddings by threshold
    indexes = [
        ind
        for sim, ind in zip(similarities, indexes)
        if ind > -1 and sim > similarity_threshold
    ]

    # retrieve file duration
    singleton_db = SingletonDB(speaker_database_path)
    duration = singleton_db.get_duration(indexes)
    return duration


def similarity_service(
        wav_content,
        embedding,
        speaker_index_path,
        speaker_database_path,
        wav_base_folder,
        embedding_size,
        max_speaker_duration,
        similarity_threshold
):
    # search faiss for similar embeddings
    duration = get_speaker_duration(
        embedding,
        speaker_index_path,
        speaker_database_path,
        embedding_size,
        max_speaker_duration,
        similarity_threshold
    )
    singleton_faiss = SingletonFaiss(speaker_index_path, embedding_size)
    singleton_db = SingletonDB(speaker_database_path)

    print(f'speaker duration: {duration}')
    if duration > max_speaker_duration:
        return {'staus': 'enough data from this speaker'}

    # insert data
    file_name = uuid.uuid4().hex + '.wav'
    with open(os.path.join(wav_base_folder, file_name), 'wb') as f:
        f.write(wav_content)
    file_handler = io.BytesIO(wav_content)
    x, sr = sf.read(file_handler)
    duration = x.shape[0] / sr
    embedding = convert_to_np(embedding)
    singleton_faiss.insert(embedding)
    singleton_faiss.save_index()
    singleton_db.execute_write_query(file_name, duration)
    return {'status': 'OK', 'filename': file_name}
