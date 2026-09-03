FROM debian:bookworm

# Install MariaDB
RUN apt-get update && \
    apt-get install -y mariadb-server && \
    rm -rf /var/lib/apt/lists/*

# Create the runtime directory used by MariaDB
RUN mkdir -p /run/mysqld && \
    chown mysql:mysql /run/mysqld

# Copy MariaDB configuration
COPY conf/my.cnf /etc/mysql/mariadb.conf.d/99-custom.cnf

# Copy the startup script
COPY tools/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 3306

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]