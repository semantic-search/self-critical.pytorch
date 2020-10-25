## RUN IMAGE DIRECTLY

Clone Repo locally

```git
    git clone --recurse-submodules https://github.com/semantic-search/self-critical.pytorch.git
```

Run compose file
```
docker-compose up
```

## TO Build consumer image and debug 

comment image in docker compose file and do below commands

```
docker-compose build
```

```
docker-compose up
```