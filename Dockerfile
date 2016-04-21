FROM ubuntu:16.04
MAINTAINER Musician Stash Developers <devs@musicianstash.com>

WORKDIR /srv/crawler

RUN apt-get update && \
    apt-get install -y curl python3-pip python3-dev python3-lxml-dbg build-essential libssl-dev libffi-dev && \
    apt-get clean

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
