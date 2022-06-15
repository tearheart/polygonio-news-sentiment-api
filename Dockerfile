FROM python:3.8-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8160

CMD ["uvicorn", "src.main:app", "--host","0.0.0.0","--port","8160"]
