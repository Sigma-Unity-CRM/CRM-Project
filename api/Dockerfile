FROM python:3.10-bullseye

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py

# Uncomment and modify these lines as you add subdirectories to your project
# COPY queries queries
# COPY routers routers
# COPY migrations migrations

RUN python -m pip install -r requirements.txt

CMD python -m migrations up && uvicorn main:app --host 0.0.0.0 --port 80 --forwarded-allow-ips "*"
