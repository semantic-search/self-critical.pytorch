FROM akshay090/self-critical.pytorch:latest

# Set the locale
ENV LANG=C.UTF-8  
ENV LC_ALL=C.UTF-8

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
