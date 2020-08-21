## Docker GPU Image of [self-critical.pytorch](https://github.com/ruotianluo/self-critical.pytorch)

Base Image 
```
docker pull akshay090/self-critical.pytorch:latest
```

API Image
```
docker build -t self-critical .
```
Run 

```
docker run --gpus all --env-file .env -it self-critical bash
```
