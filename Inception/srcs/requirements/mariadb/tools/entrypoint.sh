#!/bin/bash
set -e

# Read passwords from secrets, stripping CRLF
if [ -f /run/secrets/db_root_password ]; then
    MYSQL_ROOT_PASSWORD="$(tr -d '\r\n' < /run/secrets/db_root_password)"
fi
if [ -f /run/secrets/db_password ]; then
    ADMIN_PASS="$(tr -d '\r\n' < /run/secrets/db_password)"
fi
if [ -f /run/secrets/db_password_2 ]; then
    MYSQL_PASSWORD="$(tr -d '\r\n' < /run/secrets/db_password_2)"
fi

DATADIR="/var/lib/mysql"

# Ensure runtime directories exist and have proper ownership
mkdir -p /run/mysqld "$DATADIR"
chown -R mysql:mysql /run/mysqld "$DATADIR"
chmod 777 /run/mysqld

# Clean up stale socket or pid files from unclean shutdowns
rm -f /run/mysqld/mysqld.sock /run/mysqld/mysqld.pid

if [ ! -d "$DATADIR/mysql" ]; then
    echo "Initializing MariaDB data directory..."
    mysql_install_db --user=mysql --datadir="$DATADIR" --rpm > /dev/null 2>&1

    mysqld --user=mysql --skip-networking --socket=/run/mysqld/mysqld.sock &
    pid="$!"

    until mysqladmin --socket=/run/mysqld/mysqld.sock ping --silent; do
        sleep 1
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

    mysqladmin --socket=/run/mysqld/mysqld.sock -u root -p"${MYSQL_ROOT_PASSWORD}" shutdown
    wait "$pid"
    echo "MariaDB initialization completed."
fi

# Ensure correct permissions on data directory before startup
chown -R mysql:mysql /run/mysqld "$DATADIR"

echo "Starting MariaDB..."
exec mysqld --user=mysql
