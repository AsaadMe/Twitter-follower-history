FROM python:alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./follower_history.py ./app.py ./accounts.txt database_com.py ./
COPY templates templates

EXPOSE 5000
CMD python app.py