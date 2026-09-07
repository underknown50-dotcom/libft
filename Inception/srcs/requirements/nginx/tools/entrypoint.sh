#!/bin/bash
set -e

DOMAIN="${DOMAIN_NAME:-mewaysi.42.fr}"

# Generate self-signed TLS certificate if not already present
if [ ! -f /etc/ssl/certs/nginx-selfsigned.crt ] || [ ! -f /etc/ssl/private/nginx-selfsigned.key ]; then
    echo "Generating self-signed TLS certificate for ${DOMAIN}..."
    mkdir -p /etc/ssl/certs /etc/ssl/private
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/ssl/private/nginx-selfsigned.key \
        -out /etc/ssl/certs/nginx-selfsigned.crt \
        -subj "/C=FR/ST=Paris/L=Paris/O=42/CN=${DOMAIN}"
fi

echo "Starting NGINX..."
exec nginx -g "daemon off;"
