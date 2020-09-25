FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential netcat vim-tiny jq python3-dev git && \
    pip install -r requirements.txt
COPY . .
CMD ["/code/start.sh"]
