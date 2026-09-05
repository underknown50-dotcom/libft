FROM debian:bookworm

RUN apt-get update && \
    apt-get install -y mariadb-server && \
    rm -rf /var/lib/apt/lists/* && rm -rf /var/lib/mysql/*

RUN mkdir -p /run/mysqld && \
    chown mysql:mysql /run/mysqld

COPY conf/my.cnf /etc/mysql/mariadb.conf.d/99-custom.cnf

COPY tools/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 3306

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]