#!/bin/bash

if [ -f /run/secrets/db_root_password ]; then
    MYSQL_ROOT_PASSWORD="$(cat /run/secrets/db_root_password)"
fi
if [ -f /run/secrets/db_password ]; then
    ADMIN_PASS="$(cat /run/secrets/db_password)"
fi
if [ -f /run/secrets/db_password_2 ]; then
    MYSQL_PASSWORD="$(cat /run/secrets/db_password_2)"
fi

DATADIR="/var/lib/mysql"

if [ ! -d "$DATADIR/mysql" ]; then
    echo "Initializing MariaDB data directory..."
    mysql_install_db --user=mysql --datadir="$DATADIR" > /dev/null 2>&1

    mysqld --skip-networking --socket=/run/mysqld/mysqld.sock &
    pid="$!"

    until mysqladmin --socket=/run/mysqld/mysqld.sock ping --silent; do
        sleep 2
    done

    echo "Bootstrapping database and users..."
    mysql --socket=/run/mysqld/mysqld.sock <<-EOSQL
        DELETE FROM mysql.user WHERE User='';
        DROP DATABASE IF EXISTS test;
        DELETE FROM mysql.db WHERE Db='test' OR Db='test\_%';

        ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';

        CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\`;

        CREATE USER IF NOT EXISTS '${ADMIN_USER}'@'%' IDENTIFIED BY '${ADMIN_PASS}';
        GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO '${ADMIN_USER}'@'%';

        CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
        GRANT SELECT, INSERT, UPDATE, DELETE ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'%';

        FLUSH PRIVILEGES;
EOSQL

    mysqladmin --socket=/run/mysqld/mysqld.sock -uroot -p"${MYSQL_ROOT_PASSWORD}" shutdown
    wait "$pid"
    echo "MariaDB initialization completed."
fi

exec mysqld
