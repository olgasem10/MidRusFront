FROM python:3.6.12-alpine


RUN mkdir /app

COPY . /app

WORKDIR /app

RUN apk add --no-cache build-base

RUN apk add --no-cache libstdc++

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["api.py"]
