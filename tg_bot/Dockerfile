FROM python:3.11-slim
# get BOT_NAME from .env.tgbot !
ENV MY_DIR=tg_bot

WORKDIR /app/${MY_DIR}

COPY requirements.txt /app/${MY_DIR}
RUN pip install -r /app/${MY_DIR}/requirements.txt


COPY entrypoint.sh .
RUN chmod u+x entrypoint.sh

COPY entrypoint-bot.sh .
RUN chmod u+x entrypoint-bot.sh

COPY entrypoint-worker.sh .
RUN chmod u+x entrypoint-worker.sh

COPY . /app/${MY_DIR}

ENTRYPOINT ./entrypoint.sh