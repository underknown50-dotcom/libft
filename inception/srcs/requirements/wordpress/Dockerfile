FROM debian:bookworm-slim

# Install php8.2-fpm, ca-certificates, required extensions, database client, and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    php8.2-fpm \
    php8.2-mysql \
    php8.2-curl \
    php8.2-gd \
    php8.2-mbstring \
    php8.2-xml \
    php8.2-xmlrpc \
    php8.2-soap \
    php8.2-intl \
    php8.2-zip \
    mariadb-client \
    wget \
    unzip \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install WP-CLI
RUN wget -O /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
    && chmod +x /usr/local/bin/wp

# Download and extract WordPress core directly into /var/www/html
RUN wget -O /tmp/wordpress.zip https://wordpress.org/latest.zip \
    && mkdir -p /var/www/wordpress \
    && unzip /tmp/wordpress.zip -d /tmp/ \
    && mv /tmp/wordpress/* /var/www/wordpress/ \
    && rm -rf /tmp/wordpress /tmp/wordpress.zip \
    && chown -R www-data:www-data /var/www/wordpress

# Copy custom php-fpm pool config
COPY conf/www.conf /etc/php/8.2/fpm/pool.d/www.conf

# Copy entrypoint script
COPY tools/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 9000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]