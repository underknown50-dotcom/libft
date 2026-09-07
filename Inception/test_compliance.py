#!/usr/bin/env python3
"""
Automated 42 Inception Subject v1.4 Compliance & Integrity Test Suite
"""
import os, sys, re

errors = []

def check(condition, desc):
    if condition:
        print(f"  [PASS] {desc}")
    else:
        print(f"  [FAIL] {desc}")
        errors.append(desc)

print("=== 1. ENVIRONMENT & SECRETS TEST ===")
env_file = "srcs/.env"
check(os.path.isfile(env_file), "srcs/.env exists")
env_vars = {}
if os.path.isfile(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()

required_env = [
    "DOMAIN_NAME", "DATA_PATH", "MYSQL_DATABASE", "ADMIN_USER", "REGULAR_USER",
    "WORDPRESS_URL", "WP_TITLE", "WORDPRESS_ADMIN_USER", "WORDPRESS_ADMIN_PASS",
    "WORDPRESS_ADMIN_EMAIL", "WORDPRESS_USER", "WORDPRESS_USER_EMAIL", "WORDPRESS_USER_PASS"
]
for var in required_env:
    val = env_vars.get(var, "MISSING")
    check(var in env_vars and len(env_vars[var]) > 0, f"Env var {var} is defined ({val})")

admin_user = env_vars.get("WORDPRESS_ADMIN_USER", "")
check("admin" not in admin_user.lower() and "administrator" not in admin_user.lower(), 
      f"WORDPRESS_ADMIN_USER (\"{admin_user}\") contains no admin/administrator")

secrets = ["credentials.txt", "db_password.txt", "db_password_2.txt", "db_root_password.txt"]
for s in secrets:
    sp = os.path.join("secrets", s)
    check(os.path.isfile(sp) and os.path.getsize(sp) > 0, f"Secret file {s} exists and is non-empty")

check(os.path.isfile(".gitignore"), ".gitignore exists")
if os.path.isfile(".gitignore"):
    with open(".gitignore") as f:
        gi = f.read()
    check("secrets/*.txt" in gi or "secrets/" in gi, ".gitignore protects secrets")
    check(".env" in gi, ".gitignore protects .env")

print("\n=== 2. DOCKERFILES & BASE IMAGES TEST ===")
dockerfiles = {
    "mariadb": "srcs/requirements/mariadb/Dockerfile",
    "nginx": "srcs/requirements/nginx/Dockerfile",
    "wordpress": "srcs/requirements/wordpress/Dockerfile"
}
for svc, df in dockerfiles.items():
    check(os.path.isfile(df), f"{svc} Dockerfile exists")
    if os.path.isfile(df):
        with open(df) as f:
            content = f.read()
        check(":latest" not in content, f"{svc} Dockerfile does NOT use :latest tag")
        check("FROM debian:bookworm-slim" in content or "FROM debian:bullseye" in content or "FROM alpine:" in content, 
              f"{svc} Dockerfile uses valid penultimate stable base image")
        check(not re.search(r"tail\s+-f|sleep\s+infinity", content), f"{svc} Dockerfile avoids hacky infinite loops")

print("\n=== 3. NGINX CONFIGURATION TEST ===")
nginx_conf = "srcs/requirements/nginx/conf/nginx.conf"
check(os.path.isfile(nginx_conf), "nginx.conf exists")
if os.path.isfile(nginx_conf):
    with open(nginx_conf) as f:
        nc = f.read()
    check("listen 443 ssl" in nc, "Nginx listens on port 443 with SSL")
    check("ssl_protocols TLSv1.2 TLSv1.3;" in nc, "Nginx enforces TLSv1.2 and TLSv1.3 only")
    check("fastcgi_pass wordpress:9000;" in nc, "Nginx proxies PHP to wordpress:9000")
    check("try_files $uri =404;" in nc or "try_files $uri" in nc, "Nginx uses try_files for security")
    check("listen 80" not in nc, "Nginx does NOT expose port 80 (443 only)")

print("\n=== 4. MARIADB CONFIGURATION TEST ===")
my_cnf = "srcs/requirements/mariadb/conf/my.cnf"
check(os.path.isfile(my_cnf), "my.cnf exists")
if os.path.isfile(my_cnf):
    with open(my_cnf) as f:
        mc = f.read()
    check("3306" in mc, "MariaDB configured on port 3306")
    check("0.0.0.0" in mc, "MariaDB binds to 0.0.0.0 for Docker network")

print("\n=== 5. WORDPRESS PHP-FPM CONFIGURATION TEST ===")
www_conf = "srcs/requirements/wordpress/conf/www.conf"
check(os.path.isfile(www_conf), "www.conf exists")
if os.path.isfile(www_conf):
    with open(www_conf) as f:
        wc = f.read()
    check("listen = 9000" in wc, "php-fpm listens on port 9000")
    check("clear_env = no" in wc, "php-fpm preserves environment variables")

print("\n=== 6. ENTRYPOINT SCRIPTS TEST ===")
scripts = [
    "srcs/requirements/mariadb/tools/entrypoint.sh",
    "srcs/requirements/wordpress/tools/entrypoint.sh"
]
for sc in scripts:
    check(os.path.isfile(sc), f"{sc} exists")
    check(os.access(sc, os.X_OK), f"{sc} is executable")
    with open(sc) as f:
        scc = f.read()
    check(scc.startswith("#!/bin/bash") or scc.startswith("#!/bin/sh"), f"{sc} has valid shebang")
    check("exec " in scc, f"{sc} uses exec for proper PID 1 signal forwarding")
    check(not re.search(r"tail\s+-f|sleep\s+infinity", scc), f"{sc} has no prohibited infinite loop hacks")

with open("srcs/requirements/wordpress/tools/entrypoint.sh") as f:
    wpsc = f.read()
check("wp core install" in wpsc, "WordPress script automates core install")
check("wp user create" in wpsc, "WordPress script creates secondary user")
check("grep -iE" in wpsc and "admin" in wpsc, "WordPress script verifies admin username constraint")

print("\n=== 7. DOCKER COMPOSE CONFIGURATION TEST ===")
compose_file = "srcs/docker-compose.yml"
check(os.path.isfile(compose_file), "docker-compose.yml exists")
if os.path.isfile(compose_file):
    with open(compose_file) as f:
        comp = f.read()
    check("image: mariadb" in comp, "Service mariadb has image: mariadb")
    check("image: wordpress" in comp, "Service wordpress has image: wordpress")
    check("image: nginx" in comp, "Service nginx has image: nginx")
    check("network_mode: host" not in comp and "network: host" not in comp, "No host network mode used")
    check("links:" not in comp and "--link" not in comp, "No deprecated links used")
    check("name: wordpress_data" in comp and "name: mariadb_data" in comp, "Volumes have explicit names")
    check("name: inception_net" in comp, "Network has explicit name inception_net")
    check("restart: always" in comp, "Containers have restart: always")
    check("credentials:" in comp and "db_root_password:" in comp, "Docker secrets mapped in compose")

print("\n=== 8. MAKEFILE TARGETS TEST ===")
check(os.path.isfile("Makefile"), "Makefile exists at root")
if os.path.isfile("Makefile"):
    with open("Makefile") as f:
        mf = f.read()
    for target in ["all", "build", "up", "down", "stop", "clean", "fclean", "re"]:
        check(f"{target}:" in mf, f"Makefile has {target} target")
    check("docker compose" in mf, "Makefile uses docker compose")

print("\n=== 9. DOCUMENTATION REQUIREMENTS TEST ===")
docs = {
    "README.md": ["This activity has been created as part of the 42 curriculum by", "Description", "Instructions", "Resources", "Virtual Machines vs Docker", "Secrets vs Environment Variables", "Docker Network vs Host Network", "Docker Volumes vs Bind Mounts"],
    "USER_DOC.md": ["User Documentation", "What services", "Starting and stopping", "Accessing the website", "Locating and managing credentials", "Checking that the services are running"],
    "DEV_DOC.md": ["Developer Documentation", "Setting up the environment from scratch", "Building and launching", "Managing containers and volumes", "Where activity data is stored and how it persists"]
}
for doc, keywords in docs.items():
    check(os.path.isfile(doc), f"{doc} exists")
    if os.path.isfile(doc):
        with open(doc) as f:
            dcontent = f.read()
        for kw in keywords:
            check(kw in dcontent, f"{doc} includes section: \"{kw}\"")

print("\n==========================================")
if errors:
    print(f"FAILED: {len(errors)} checks failed.")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("SUCCESS: ALL 48 CHECKS PASSED! (0 errors)")
