FROM debian:bullseye-slim


ARG DEBIAN_FRONTEND=noninteractive

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    wget build-essential pkg-config erlang libicu-dev libcurl4-openssl-dev libnspr4 ca-certificates; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /usr/lib/erlang/man/man*;

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends gosu tini; \
    rm -rf /var/lib/apt/lists/*; \
    gosu nobody true; \
    tini --version

WORKDIR "/home/"

RUN set-eux; \
    apt-get update -y; \
    apt-get install -y libffi-dev libnspr4-dev; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /usr/lib/erlang/man/man*;


# Install libmozjs185-dev and dependencies libmozjs185-1.0, libffi6
RUN    wget -4 -T 60 http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi6_3.2.1-6_armhf.deb; \
    wget -4 -T 60 http://ftp.ro.debian.org/debian/pool/main/m/mozjs/libmozjs185-1.0_1.8.5-1.0.0+dfsg-6_armhf.deb; \
    wget -4 -T 60 http://ftp.br.debian.org/debian/pool/main/m/mozjs/libmozjs185-dev_1.8.5-1.0.0+dfsg-6_armhf.deb; \
    dpkg -i libffi6_3.2.1-6_armhf.deb; \
    dpkg -i libmozjs185-1.0_1.8.5-1.0.0+dfsg-6_armhf.deb; \
    dpkg -i libmozjs185-dev_1.8.5-1.0.0+dfsg-6_armhf.deb; \
    mkdir /opt/couchdb/

RUN  apt-get --fix-broken install -y;

RUN set -eux; \
    wget -4 -T 60 https://dlcdn.apache.org/couchdb/source/3.2.2/apache-couchdb-3.2.2.tar.gz; \
    mkdir /home/couchdb/; \
    tar zxvf apache-couchdb-3.2.2.tar.gz -C /home/couchdb/;

WORKDIR /home/couchdb/apache-couchdb-3.2.2/

RUN ./configure
RUN make release

RUN mv /home/couchdb/apache-couchdb-3.2.2/rel/couchdb /home/couchdb/


WORKDIR /home/
RUN rm apache-couchdb-3.2.2.tar.gz libffi6_3.2.1-6_armhf.deb libmozjs185-dev_1.8.5-1.0.0+dfsg-6_armhf.deb libmozjs185-1.0_1.8.5-1.0.0+dfsg-6_armhf.deb

#TODO use tini
#ENTRYPOINT ["/tini", "--"]

EXPOSE 5984 4369 9100

CMD ["/home/couchdb/couchdb/bin/couchdb"]



