#!/bin/bash

# Read passwords from Docker secrets or environment variables
if [ -f /run/secrets/db_root_password ]; then
    MYSQL_ROOT_PASSWORD="$(cat /run/secrets/db_root_password)"
fi
if [ -f /run/secrets/db_regular_password ]; then
    MYSQL_PASSWORD="$(cat /run/secrets/db_regular_password)"
fi

# Path where MariaDB stores system tables
DATADIR="/var/lib/mysql"

# Initialize database if not already done
if [ ! -d "$DATADIR/mysql" ]; then
    echo "Initializing MariaDB data directory..."
    mysql_install_db --user=mysql --datadir="$DATADIR" > /dev/null 2>&1

    # Start temporary mysqld instance in the background for bootstrapping
    mysqld --skip-networking --socket=/run/mysqld/mysqld.sock &
    pid="$!"

    # Wait for the temp server to be ready
    until mysqladmin --socket=/run/mysqld/mysqld.sock ping --silent; do
        sleep 2
    done

    echo "Bootstrapping database and users..."
    mysql --socket=/run/mysqld/mysqld.sock <<-EOSQL
        DELETE FROM mysql.user WHERE User='';
        DROP DATABASE IF EXISTS test;
        DELETE FROM mysql.db WHERE Db='test' OR Db='test\_%';
        
        -- Set root password securely
        ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';
        
        -- Create WordPress database
        CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\`;
        
        -- Create WordPress user and grant privileges
        CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
        GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'%';
        
        FLUSH PRIVILEGES;
EOSQL

    # Gracefully shutdown the temporary background mysqld instance
    mysqladmin --socket=/run/mysqld/mysqld.sock shutdown
    wait "$pid"
    echo "MariaDB initialization completed."
fi

# Start MariaDB server normally in the foreground
exec mysqld
