FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade --no-cache-dir requests

COPY "entrypoint.sh" "/entrypoint.sh"
COPY "upload.py"    "/upload.py"
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]