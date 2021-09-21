FROM python

WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./follower_history.py ./app.py ./accounts.txt database_com.py ./
COPY templates templates

EXPOSE 5000
CMD python app.py