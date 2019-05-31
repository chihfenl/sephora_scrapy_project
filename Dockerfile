FROM python:3.7-alpine3.8

ENV PATH /usr/local/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/lib

RUN mkdir /apps

WORKDIR /apps

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.8/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.8/community" >> /etc/apk/repositories

RUN apk add --update --no-cache \ 
    gcc \
    tzdata \
    curl \
    unzip \
    openssl-dev \
    libxml2 \
    libxml2-dev \
    libffi \
    libffi-dev \
    libxslt-dev \
    build-base \
    python-dev \
    py-pip \
    vim \
    jpeg-dev \
    zlib-dev \
    chromium \
    libexif \
    udev \
    chromium-chromedriver

COPY requirements.txt ./

RUN pip install -r requirements.txt \
    && rm -rf /var/cache/apk/*

COPY . .

CMD scrapy crawl sephora_test
