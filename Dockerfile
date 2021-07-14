FROM python:3

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt 

EXPOSE 8000

RUN python /app/validate/manage.py check --deploy

STOPSIGNAL SIGTERM

CMD ["/app/startserver.sh"]

