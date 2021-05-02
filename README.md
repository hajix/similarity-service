# Similarity Service for Audio Data Gathering

## How to run the service:

1. Build docker image: `docker build -t similarity-service:v1.0 .`

2. run container: `run.sh`

## Sample request:

```python
import requests

with open('path/to/wav', 'rb') as f:
    data = f.read()

files = { 'wav_content': ('George-crop2.wav;type', data), }
params = (('embedding', b64_emb_string), )

response = requests.post(
    'http://localhost:8017/similarity_service',
    files=files,
    params=params
)
```
