FROM ubuntu:14.04
MAINTAINER Musician Stash Developers <devs@musicianstash.com>

WORKDIR /srv/crawler

RUN apt-get update && \
    apt-get install -y curl python-pip python-dev python-lxml-dbg build-essential libssl-dev libffi-dev && \
    apt-get clean

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
