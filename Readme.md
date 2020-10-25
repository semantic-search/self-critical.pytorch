## RUN IMAGE DIRECTLY

Clone Repo locally

```git
    git clone --recurse-submodules https://github.com/semantic-search/self-critical.pytorch.git
```

Pull images
```
docker-compose pull
```

Run compose file
```
docker-compose up
```

## TO Build consumer image and debug 

add below line in kafka-consumer in docker-compose.yaml

```
    build:
      context: ./
      dockerfile: ./Dockerfile
```
