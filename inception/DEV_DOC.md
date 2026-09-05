# Developer Documentation

This document explains how to set up, build, and maintain the Inception
stack from a developer's point of view.

## Setting up the environment from scratch

### Prerequisites

- A Linux virtual machine with Docker Engine and the Docker Compose plugin
  installed.
- `sudo` privileges (the Makefile's `build` target creates and `chown`s the
  host data directories).

### Repository layout

```
inception/
├── Makefile
├── docker-compose.yml
├── .env
├── secrets/
│   ├── db_root_password.txt
│   ├── db_password.txt
│   └── db_password_2.txt
└── srcs/
    └── requirements/
        ├── mariadb/
        │   ├── Dockerfile
        │   ├── conf/my.cnf
        │   └── tools/entrypoint.sh
        ├── nginx/
        │   ├── Dockerfile
        │   └── conf/nginx.conf
        └── wordpress/
            ├── Dockerfile
            ├── conf/www.conf
            └── tools/entrypoint.sh
```

### Configuration files

- **`.env`** (project root) — non-sensitive configuration: domain name,
  database name, usernames, WordPress admin details, and the `DATA_PATH`
  variable used for the host-side volume location. This file must match
  the `DATA_DIR` value hardcoded in the `Makefile`.
- **`secrets/*.txt`** — one password per file, plain text, no trailing
  newline (create with `echo -n "password" > secrets/name.txt`). This
  folder is `.gitignore`d and must never be committed.

Before your first build, create the three secret files:

```bash
mkdir -p secrets
echo -n "your_root_password"    > secrets/db_root_password.txt
echo -n "your_admin_password"   > secrets/db_password.txt
echo -n "your_regular_password" > secrets/db_password_2.txt
chmod 600 secrets/*.txt
```

## Building and launching via the Makefile and Docker Compose

```bash
make          # equivalent to: make build && make up
```

Internally, `make build`:
1. Creates the host data directories (`$(DATA_DIR)/wordpress`,
   `$(DATA_DIR)/mariadb`) and gives them correct ownership.
2. Runs `docker compose build`, which builds all three images from their
   respective `Dockerfile`s — no image is pulled ready-made from Docker
   Hub except the official `debian` base images.

`make up` then runs `docker compose up -d`, starting all three containers
in detached mode, connected through the `inception_net` bridge network.

Other targets:

```bash
make down     # docker compose down (containers + network removed, volumes kept)
make stop     # docker compose stop (containers stopped, not removed)
make clean    # down + docker compose rm -f
make fclean   # clean + delete the entire host data directory
make re       # fclean + all — full rebuild from a clean state
```

## Managing containers and volumes

Useful commands beyond the Makefile targets:

```bash
docker ps -a                      # list all containers and their status
docker logs <name> --tail 50      # inspect recent output of a container
docker exec -it <name> sh         # get a shell inside a running container
docker exec <name> ps -p 1        # confirm what's running as PID 1
docker compose build <service>    # rebuild a single service's image
docker volume ls                  # list Docker-managed volumes
docker volume inspect <name>      # see a volume's actual mountpoint
```

Each entrypoint script (`mariadb/tools/entrypoint.sh`,
`wordpress/tools/entrypoint.sh`) ends with an `exec` call to the actual
server process (`mysqld`, `php-fpm8.2 -F`), so that process — not the
shell script — becomes PID 1 inside its container. This is required so
that signals like `SIGTERM` (sent by `docker stop`) reach the real service
directly instead of being swallowed by a wrapping shell.

## Where activity data is stored and how it persists

The two Docker named volumes are configured (via `driver_opts` with
`type: none` / `o: bind`) to store their actual data under a specific host
path rather than Docker's default internal volume storage location:

| Named volume | Host path | Contents |
|---|---|---|
| `mariadb_data` | `${DATA_PATH}/mariadb` | MariaDB's full data directory (`/var/lib/mysql` inside the container) |
| `wordpress_files` | `${DATA_PATH}/wordpress` | WordPress core files, uploads, themes, plugins (`/var/www/wordpress` inside the container) |

Because these are true named volumes (declared under the top-level
`volumes:` key and referenced by name in each service, rather than a raw
host-path-to-container-path bind mount in a service's own `volumes:`
list), they survive `docker compose down` and container rebuilds — data is
only lost if you explicitly run `make fclean`, which deletes the entire
host data directory, or manually remove the volumes with
`docker volume rm`.

On first startup with an empty data directory, each entrypoint script
detects the absence of existing data (`/var/lib/mysql/mysql` for MariaDB,
`wp-config.php` for WordPress) and performs first-run initialization
accordingly; on every subsequent restart, that initialization is skipped
and the existing persisted data is used as-is.
