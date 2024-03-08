FROM python:3.11
ENV MY_DIR=tg_bot

WORKDIR /app/${MY_DIR}

COPY requirements.txt .
RUN pip install -r requirements.txt


#COPY tg_bot .
COPY . .

#COPY entrypoint.sh .
RUN chmod u+x entrypoint.sh

#COPY entrypoint-bot.sh .
RUN chmod u+x entrypoint-bot.sh

#COPY entrypoint-worker.sh .
RUN chmod u+x entrypoint-worker.sh




RUN useradd celery
RUN mkdir /var/run/celery
RUN mkdir /var/log/celery
RUN chmod +w /var/log/celery

#CMD ./entrypoint.sh
ENTRYPOINT ./entrypoint-bot.sh
#ENTRYPOINT ["python", "-m", "bot"]