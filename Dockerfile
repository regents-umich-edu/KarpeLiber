# In OpenShift, config bc to override with
# python:3.13-slim from openshift namespace
FROM python:3.13.7-slim
ENV PYTHONUNBUFFERED=1
# Makes directories /code and /code/staticfiles
RUN mkdir -p /code/staticfiles && chmod -R 0777 /code/staticfiles
WORKDIR /code
ARG IMAGE_TAG_TIMESTAMP
ENV IMAGE_TAG_TIMESTAMP=$IMAGE_TAG_TIMESTAMP
COPY requirements.txt .
# See packages at: https://packages.debian.org/#search_packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential netcat-traditional vim-tiny jq git socat \
        default-libmysqlclient-dev python3-numpy && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["/code/start.sh"]
