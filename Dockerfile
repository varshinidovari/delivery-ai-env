
FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install flask openenv-core

CMD ["python", "server/app.py"]
