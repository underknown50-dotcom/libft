FROM debian:bookworm-slim

# Install nginx, openssl, and procps (for ps command)
RUN apt-get update && apt-get install -y nginx openssl procps && rm -rf /var/lib/apt/lists/*

# Copy custom nginx configuration
COPY conf/nginx.conf /etc/nginx/sites-available/default

# Remove default config and enable our site
RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Copy entrypoint script
COPY tools/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 443

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
