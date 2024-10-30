FROM python:3.10-buster

WORKDIR /app/api
COPY requirements.txt /app/api/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel
RUN if [ -f /app/api/requirements.txt ]; then python -m pip install -r /app/api/requirements.txt; fi

ENTRYPOINT ["python", "server.py"]