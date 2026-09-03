#!/bin/bash

# Ensure html directory exists and belongs to www-data
mkdir -p /var/www/html
chown -R www-data:www-data /var/www/html

# If the volume is empty (shadowed by Docker volume mount), download WordPress core
if [ ! -f /var/www/html/wp-settings.php ]; then
    echo "Volume is empty. Downloading WordPress core at runtime..."
    wget -O /tmp/wordpress.zip https://wordpress.org/latest.zip
    unzip -q /tmp/wordpress.zip -d /var/www/
    cp -rn /var/www/wordpress/* /var/www/html/
    rm -rf /var/www/wordpress /tmp/wordpress.zip
    chown -R www-data:www-data /var/www/html
fi

# Wait for MariaDB to be fully ready
until mysqladmin ping -h"mariadb" -P3306 --silent; do
    echo "Waiting for database..."
    sleep 2
done

# Resolve database password from environment or mounted Docker secrets
if [ -n "$WORDPRESS_DB_PASSWORD" ]; then
    DB_PASS="$WORDPRESS_DB_PASSWORD"
elif [ -f "${WORDPRESS_DB_PASSWORD_FILE:-}" ]; then
    DB_PASS="$(cat "${WORDPRESS_DB_PASSWORD_FILE}")"
elif [ -f /run/secrets/db_regular_password ]; then
    DB_PASS="$(cat /run/secrets/db_regular_password)"
elif [ -f /run/secrets/wordpress_password ]; then
    DB_PASS="$(cat /run/secrets/wordpress_password)"
else
    DB_PASS=""
fi

DB_USER="${WORDPRESS_DB_USER:-root}"

# Navigate to WordPress directory
cd /var/www/html

# Check if WordPress configuration exists, create if missing
if [ ! -f wp-config.php ]; then
    echo "Setting up WordPress configuration..."
    
    wp config create \
        --dbname="${WORDPRESS_DB_NAME}" \
        --dbuser="${DB_USER}" \
        --dbpass="${DB_PASS}" \
        --dbhost="${WORDPRESS_DB_HOST}" \
        --allow-root

    # Install WordPress if tables don't exist yet
    if ! wp core is-installed --allow-root; then
        echo "Installing WordPress..."
        wp core install \
            --url="${DOMAIN_NAME}" \
            --title="${WP_TITLE}" \
            --admin_user="${WORDPRESS_ADMIN_USER}" \
            --admin_password="${WORDPRESS_ADMIN_PASS}" \
            --admin_email="${WORDPRESS_ADMIN_EMAIL}" \
            --allow-root
            
        wp user create \
            "${WORDPRESS_USER}" "${WORDPRESS_USER_EMAIL}" \
            --role=author \
            --user_pass="${WORDPRESS_USER_PASS}" \
            --allow-root
    fi
fi

# Ensure correct permissions for PHP-FPM
chown -R www-data:www-data /var/www/html

# Start PHP-FPM in the foreground
exec php-fpm8.2 -F
