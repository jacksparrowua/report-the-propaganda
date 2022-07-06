FROM python:3.10.0-alpine

COPY src src
COPY requirements requirements

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements/requirements.txt --no-cache-dir

CMD ["python3", "src/main.py"]