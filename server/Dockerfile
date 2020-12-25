FROM python:3

WORKDIR /app

COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app/ .

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "main:app"]
