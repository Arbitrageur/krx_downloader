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
COPY *.py /script/
COPY run /script/
RUN chmod a+x /script/run

RUN echo '0 8 * * *    /script/run' >> /etc/crontabs/root

CMD ['crond', '-l 2', 'f']
