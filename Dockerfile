FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

# COPY . /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

# RUN pip install -r requirements.txt 

# EXPOSE 8000

# RUN python /app/validate/manage.py check --deploy

# STOPSIGNAL SIGTERM

# CMD ["/app/startserver.sh"]

