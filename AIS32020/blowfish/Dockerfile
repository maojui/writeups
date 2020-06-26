FROM ubuntu:18.04

MAINTAINER maojui <maojui0427@gmail.com>

RUN apt-get -qq update
RUN apt install python3-pip -y
RUN apt-get -qqy install socat

RUN useradd -m bof
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/bof

RUN pip3 install pycrypto 

RUN mkdir -p /root/app
WORKDIR /root/app
COPY secret.py      /root/app/secret.py
COPY prob.py        /root/app/prob.py
COPY user.pickle    /root/app/user.pickle

CMD ["/usr/bin/socat","tcp-listen:12001,fork", "exec:'python3 prob.py',reuseaddr"]