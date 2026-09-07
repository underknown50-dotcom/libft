#!/bin/bash
set -e

mkdir -p /var/www/wordpress /run/php
chown -R www-data:www-data /var/www/wordpress /run/php

# If volume is empty, copy cached WordPress core from /usr/src/wordpress (fallback to download if needed)
if [ ! -f /var/www/wordpress/wp-settings.php ]; then
    echo "Volume is empty. Populating WordPress core files..."
    if [ -d /usr/src/wordpress ]; then
        cp -rn /usr/src/wordpress/* /var/www/wordpress/
    else
        wget -O /tmp/wordpress.zip https://wordpress.org/latest.zip
        unzip -q /tmp/wordpress.zip -d /tmp/
        cp -rn /tmp/wordpress/* /var/www/wordpress/
        rm -rf /tmp/wordpress /tmp/wordpress.zip
    fi
    chown -R www-data:www-data /var/www/wordpress
fi

# Resolve database password (stripping any CRLF)
if [ -n "${WORDPRESS_DB_PASSWORD:-}" ]; then
    DB_PASS="$WORDPRESS_DB_PASSWORD"
elif [ -f "${WORDPRESS_DB_PASSWORD_FILE:-}" ]; then
    DB_PASS="$(tr -d '\r\n' < "${WORDPRESS_DB_PASSWORD_FILE}")"
else
    DB_PASS=""
fi

# Resolve WordPress administrator password from secret file or environment
if [ -f "${WORDPRESS_ADMIN_PASS_FILE:-}" ]; then
    WP_ADMIN_PASS="$(tr -d '\r\n' < "${WORDPRESS_ADMIN_PASS_FILE}")"
elif [ -f /run/secrets/credentials ]; then
    WP_ADMIN_PASS="$(tr -d '\r\n' < /run/secrets/credentials)"
elif [ -n "${WORDPRESS_ADMIN_PASS:-}" ]; then
    WP_ADMIN_PASS="$WORDPRESS_ADMIN_PASS"
else
    WP_ADMIN_PASS=""
fi

# Validate subject requirement: administrator username must NOT contain admin/Admin or administrator/Administrator
if echo "${WORDPRESS_ADMIN_USER}" | grep -iE 'admin' >/dev/null 2>&1; then
    echo "ERROR: WordPress administrator username ('${WORDPRESS_ADMIN_USER}') must not contain 'admin' or 'administrator' per 42 subject rules!"
    exit 1
fi

DB_USER="${WORDPRESS_DB_USER:-root}"

# Normalize WordPress URL to ensure https:// scheme
WP_URL="${WORDPRESS_URL:-https://${DOMAIN_NAME:-mewaysi.42.fr}}"
if [[ ! "$WP_URL" =~ ^https?:// ]]; then
    WP_URL="https://${WP_URL}"
fi

# Wait for MariaDB server to be fully ready
echo "Waiting for MariaDB server to be ready..."
until mariadb-admin ping -h mariadb --silent; do
    sleep 2
done

cd /var/www/wordpress

# Create wp-config.php if not present
if [ ! -f wp-config.php ]; then
    echo "Setting up WordPress configuration..."
    wp config create \
        --dbname="${WORDPRESS_DB_NAME}" \
        --dbuser="${DB_USER}" \
        --dbpass="${DB_PASS}" \
        --dbhost="${WORDPRESS_DB_HOST}" \
        --allow-root
fi

# Run core install if WordPress is not yet installed
if ! wp core is-installed --allow-root; then
    echo "Installing WordPress..."
    wp core install \
        --url="${WP_URL}" \
        --title="${WP_TITLE:-Inception mewaysi}" \
        --admin_user="${WORDPRESS_ADMIN_USER}" \
        --admin_password="${WP_ADMIN_PASS}" \
        --admin_email="${WORDPRESS_ADMIN_EMAIL}" \
        --skip-email \
        --allow-root

    echo "Creating regular user..."
    wp user create \
        "${WORDPRESS_USER}" "${WORDPRESS_USER_EMAIL}" \
        --role=author \
        --user_pass="${WORDPRESS_USER_PASS}" \
        --allow-root
fi

chown -R www-data:www-data /var/www/wordpress /run/php

echo "Starting PHP-FPM..."
exec php-fpm8.2 -F
