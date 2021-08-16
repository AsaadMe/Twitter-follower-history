FROM python:slim

WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./follower_history.py ./app.py ./
COPY templates templates

EXPOSE 5000
CMD python app.py