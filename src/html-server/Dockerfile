FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn requests jinja2 python-multipart

COPY html-server.py .
COPY /templates/ ./templates/

EXPOSE 8000

ENV IN_CONTAINER=Yes

CMD ["uvicorn", "html-server:app", "--host", "0.0.0.0" , "--port", "8001"]