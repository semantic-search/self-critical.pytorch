## Docker GPU Image of [self-critical.pytorch](https://github.com/ruotianluo/self-critical.pytorch)

Base Image 
```
docker pull akshay090/self-critical.pytorch:latest
```
API Image
```
docker run --gpus all -it -p 80:80 akshay090/self-critical.pytorch:api
```
Test API
```
curl --location --request POST 'http://127.0.0.1:80/caption/' --form 'file=@/home/sign.jpg'
```
