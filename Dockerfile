FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app
RUN apt-get update && apt-get upgrade && apt-get install -y --no-install-recommends gcc

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .

RUN chmod a+x entry-point.sh

#COPY entrypoint.sh .
RUN chmod a+x tg_bot/entrypoint.sh

#COPY entrypoint-bot.sh .
RUN chmod a+x tg_bot/entrypoint-bot.sh

#COPY entrypoint-worker.sh .
RUN chmod a+x tg_bot/entrypoint-worker.sh




#RUN useradd celery
#RUN mkdir /var/run/celery
#RUN mkdir /var/log/celery
#RUN chmod +w /var/log/celery



#ENTRYPOINT ["entrypoint.sh"]
#ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
