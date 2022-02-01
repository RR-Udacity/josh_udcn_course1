FROM python:3.9-slim
RUN apt-get update \
        && apt-get upgrade -y \
        && apt-get install -y \
        && apt-get -y install apt-utils netcat gunicorn libpq-dev python3-dev gcc vim\
        && apt-get autoremove -y \
        && apt-get clean all

COPY ./techtrends/requirements.txt .
RUN pip install --upgrade pip -r requirements.txt
COPY ./techtrends .
RUN python -m init_db
EXPOSE 3111
CMD ["python", "-m", "app"]