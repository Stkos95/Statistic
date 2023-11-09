FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app
RUN apt-get update && apt-get upgrade && apt-get install -y --no-install-recommends gcc

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .

#ENTRYPOINT ["entrypoint.sh"]
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
