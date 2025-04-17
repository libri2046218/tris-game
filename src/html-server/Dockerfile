FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY html-server.py .
COPY /templates/ ./templates/

EXPOSE 8001

ENV IN_CONTAINER=Yes

CMD ["uvicorn", "html-server:app", "--host", "0.0.0.0" , "--port", "8001"]
