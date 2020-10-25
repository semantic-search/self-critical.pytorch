## RUN IMAGE DIRECTLY

Clone Repo locally

```git
    git clone --recurse-submodules https://github.com/semantic-search/self-critical.pytorch.git
```

RUN Prod compose file
```
docker-compose -f docker-prod.yaml up
```

## TO Build consumer image and debug 

```
docker-compose build
```

```
docker-compose up
```