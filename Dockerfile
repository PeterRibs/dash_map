FROM python:3.10

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

COPY ./app /app

CMD [ "python", "app.py" ]

EXPOSE 3000
