# In OpenShift, config bc to override with
# python:3.9-slim from openshift namespace
FROM python:3.13.7-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential netcat-traditional vim-tiny jq git socat \
        default-libmysqlclient-dev && \
    pip install -r requirements.txt
COPY . .
CMD ["/code/start.sh"]
