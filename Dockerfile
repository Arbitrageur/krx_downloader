FROM joyzoursky/python-chromedriver:3.7-alpine3.8-selenium

LABEL maintainer="yeolhyun.kwon@gmail.com"

ENV GITHUB_USER=nobody
ENV GITHUB_REPO=nowhere
ENV KRX_USER=someone
ENV KRX_PASS=secret
ENV PASSPHRASE=passphrase

RUN apk update
RUN apk add git openssh-client

RUN apk add build-base

RUN pip install pycryptodomex

RUN mkdir /secrets
VOLUME /secrets

WORKDIR /root
RUN mkdir .ssh

RUN mkdir /script
WORKDIR /script
ADD *.py /script/
ADD run /script/
ADD crontab /script/
RUN chmod 755 /script/crontab
RUN /usr/bin/crontab /script/crontab

ADD entry /script/
RUN chmod 755 /script/run
RUN chmod 755 /script/entry

CMD ["/script/entry"]
