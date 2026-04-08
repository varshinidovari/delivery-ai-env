FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install flask openenv openai requests

CMD ["python", "server/app.py"]
