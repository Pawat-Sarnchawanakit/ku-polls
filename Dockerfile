FROM python:3-alpine

WORKDIR /app/ku-polls
COPY . .

RUN pip install -r requirements.txt
RUN cat sample.env > .env

EXPOSE 8000
CMD [ "python", "entrypoint.py" ]
