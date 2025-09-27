# In OpenShift, config bc to override with
# python:3.13-slim from openshift namespace
FROM python:3.13.7-slim
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
# See packages at: https://packages.debian.org/#search_packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential netcat-traditional vim-tiny jq git socat \
        default-libmysqlclient-dev python3-numpy && \
    pip install -r requirements.txt
COPY . .
CMD ["/code/start.sh"]
