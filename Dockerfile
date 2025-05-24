FROM python:3.11-slim

# Allow logs to be seen by Render
ENV PYTHONUNBUFFERED True

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD exec uvicorn main:app --host 0.0.0.0 --port 10000
