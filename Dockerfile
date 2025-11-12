# In OpenShift, config bc to override with
# python:3.13-slim from openshift namespace
FROM python:3.13.9-slim
ENV PYTHONUNBUFFERED=1
# Makes directories /code and /code/staticfiles
RUN mkdir -p /code/staticfiles && chmod -R 0775 /code/staticfiles
WORKDIR /code
ARG IMAGE_TAG
ENV IMAGE_TAG=$IMAGE_TAG
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
