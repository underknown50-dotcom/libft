*This activity has been created as part of the 42 curriculum by mewaysi.*

# Inception

## Description

Inception is a system administration project whose goal is to deploy a small
web infrastructure entirely through Docker, using `docker compose`, without
relying on any pre-built images from Docker Hub (aside from the official
Alpine/Debian base images).

The infrastructure is made up of three custom-built Docker images, each
running in its own dedicated container:

- **NGINX** — the single entrypoint into the infrastructure, exposing port
  443 over TLSv1.2/TLSv1.3 only.
- **WordPress + php-fpm** — the WordPress application, served through
  php-fpm (no web server bundled in this container).
- **MariaDB** — the database backing WordPress.

The containers communicate with each other exclusively through a dedicated
Docker network (`inception_net`), and persist their data through two Docker
named volumes (one for the database, one for the WordPress site files), both
backed by a specific directory on the host machine.

## Instructions

### Prerequisites

- A Linux virtual machine with Docker and Docker Compose installed.
- Your login's domain name (`<login>.42.fr`) must resolve to the VM's local
  IP address (e.g. via an `/etc/hosts` entry).

### Setup

1. Clone this repository onto your virtual machine.
2. Create the `secrets/` folder at the project root (already `.gitignore`d)
   containing the following plain-text files, one password per file, no
   trailing newline:
   - `db_root_password.txt`
   - `db_password.txt`
   - `db_password_2.txt`
   - `credentials.txt`
3. Adjust `srcs/.env` (copied from `srcs/.env.example` if necessary) to
   match your login, domain, database name, and usernames. Ensure the
   WordPress administrator username does NOT contain `admin` or `administrator`.

### Build and run

```bash
make          # builds all images and starts the stack in detached mode
```

Other available targets:

```bash
make down     # stop and remove containers + network
make stop     # stop containers without removing them
make clean    # stop everything and remove containers/network (volumes kept)
make fclean   # clean + delete the host data directory entirely
make re       # fclean + all (full rebuild from scratch)
```

Once running, visit `https://<login>.42.fr` in a browser.

## Resources

- [Docker documentation](https://docs.docker.com/)
- [Docker Compose file reference](https://docs.docker.com/compose/compose-file/)
- [MariaDB server documentation](https://mariadb.com/kb/en/documentation/)
- [WP-CLI documentation](https://wp-cli.org/)
- [NGINX documentation](https://nginx.org/en/docs/)
- [Debian package archive](https://packages.debian.org/) — used to check
  available package versions for `bookworm`.

**AI usage:** An AI assistant (Claude) was used throughout this project as a
learning and debugging aid, not as a code generator to copy-paste blindly.
Specifically, it was used to:

- Explain Docker concepts already touched on but not fully understood
  beforehand — image layers and build caching, the PID 1 problem and why
  daemonizing/`tail -f`-style hacks are forbidden, privilege dropping in
  MariaDB/php-fpm, and the difference between Docker secrets, environment
  variables, named volumes, and bind mounts.
- Review and debug the entrypoint scripts and `docker-compose.yml` after
  real build/runtime failures (e.g. a PHP version mismatch between the
  subject's older reference material and Debian bookworm's actual available
  packages, a mismatched username between the MariaDB and WordPress
  containers, and a missing secret file wiring for the WordPress database
  password).
- Ask "hard questions" about specific lines of the Dockerfiles and
  entrypoint scripts, as a self-check exercise before peer review, in line
  with the project's own AI Instructions chapter.

Every fix suggested was tested against the actual running containers before
being kept, and the reasoning behind each one was worked through rather than
applied without understanding — logs, `ps -p 1` checks, and manual SQL/DB
login tests were used throughout to verify behavior first-hand.

## Project description

### Virtual Machines vs Docker

A virtual machine virtualizes an entire hardware stack and runs a full,
independent guest operating system on top of a hypervisor — heavy in terms
of disk space, memory, and boot time, but strongly isolated from the host
and from other VMs. Docker containers, by contrast, share the host
machine's kernel and only isolate processes, filesystems, and network
namespaces from one another. This makes containers far lighter and faster
to start, at the cost of a slightly weaker isolation boundary than a full
VM. Inception was built with Docker specifically because each service
(NGINX, WordPress, MariaDB) only needs its own process and files isolated
from the others — running each in a full VM would be needlessly heavy for
that purpose.

### Secrets vs Environment Variables

Environment variables are visible to anyone with access to the container
(via `docker inspect`, `/proc/<pid>/environ`, or `docker compose config`),
and are also often stored in plain text in `.env` files that can end up
committed to version control by mistake. Docker secrets, on the other hand,
are mounted as files inside the container (under `/run/secrets/`) and are
not exposed through `docker inspect` or process environment listings. In
this project, non-sensitive configuration (hostnames, database names,
usernames) is passed via environment variables and a `.env` file, while all
passwords are stored in individual files under `secrets/` (excluded from
git) and read at container startup through `*_FILE` environment variables
pointing at the mounted secret paths.

### Docker Network vs Host Network

Using `network: host` would make a container share the host's network
stack directly, exposing every port the container binds to straight onto
the host without any isolation — and it is explicitly forbidden by the
subject. A user-defined Docker bridge network (`inception_net` here)
instead gives each container its own network namespace and a private IP
that's only reachable from other containers on the same network, with
Docker's built-in DNS letting containers reach each other by service name
(e.g. `wordpress:9000`, `mariadb:3306`). This keeps internal traffic between
WordPress, MariaDB, and NGINX inaccessible from outside the Docker host
entirely, except through whatever port NGINX itself explicitly publishes
(443).

### Docker Volumes vs Bind Mounts

A bind mount maps an arbitrary path on the host directly into the
container, with the host's filesystem in full control of permissions and
existence of that path — fragile and hard to manage safely. A named volume
is instead created and managed by Docker itself, referenced by name rather
than by path, and (via `driver_opts`) can still be configured to store its
actual data under a specific host directory. This project uses two named
volumes — `wordpress_data` and `mariadb_data` — both configured to persist
their data under `/home/mewaysi/data/`, satisfying both the "must be a
named volume" and the "must live under a specific host path" requirements
of the subject at the same time.
