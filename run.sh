docker run -d \
    -v $(pwd)/resources:/resources \
    -v $(pwd)/wav:/wav \
    -p 8017:8017 \
    -e LC_ALL=C.UTF-8 \
    --name similarity-service \
    similarity-service:v1.0
