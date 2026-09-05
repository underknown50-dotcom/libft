#!/bin/bash

mkdir -p /var/www/wordpress
chown -R www-data:www-data /var/www/wordpress

if [ ! -f /var/www/wordpress/wp-settings.php ]; then
    echo "Volume is empty. Downloading WordPress core at runtime..."
    wget -O /tmp/wordpress.zip https://wordpress.org/latest.zip
    unzip -q /tmp/wordpress.zip -d /tmp/
    cp -rn /tmp/wordpress/* /var/www/wordpress/
    rm -rf /tmp/wordpress /tmp/wordpress.zip
    chown -R www-data:www-data /var/www/wordpress
fi

until nc -z mariadb 3306; do
    echo "Waiting for database..."
    sleep 2
done

if [ -n "$WORDPRESS_DB_PASSWORD" ]; then
    DB_PASS="$WORDPRESS_DB_PASSWORD"
elif [ -f "${WORDPRESS_DB_PASSWORD_FILE:-}" ]; then
    DB_PASS="$(cat "${WORDPRESS_DB_PASSWORD_FILE}")"
else
    DB_PASS=""
fi

DB_USER="${WORDPRESS_DB_USER:-root}"

cd /var/www/wordpress

if [ ! -f wp-config.php ]; then
    echo "Setting up WordPress configuration..."

    wp config create \
        --dbname="${WORDPRESS_DB_NAME}" \
        --dbuser="${DB_USER}" \
        --dbpass="${DB_PASS}" \
        --dbhost="${WORDPRESS_DB_HOST}" \
        --allow-root

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

chown -R www-data:www-data /var/www/wordpress

exec php-fpm8.2 -F
