# User Documentation

This document explains how to use the Inception stack as an end user or
site administrator — no development knowledge required.

## What services does this stack provide?

The stack runs a fully working WordPress website, made up of three parts
working together behind the scenes:

- A **web server** (NGINX) that handles all secure (HTTPS) traffic.
- A **WordPress application** where the actual site content, pages, and
  admin panel live.
- A **database** (MariaDB) that stores everything WordPress needs: posts,
  pages, users, settings.

You don't interact with WordPress or MariaDB directly — everything is
reached through the website itself, over HTTPS.

## Starting and stopping the activity

From the project's root folder, on the virtual machine:

```bash
make          # builds (if needed) and starts everything
```

To stop the site without deleting any data:

```bash
make stop
```

To stop and remove the containers (your data is kept):

```bash
make down
```

To completely wipe everything, including all stored data:

```bash
make fclean
```

## Accessing the website and the administration panel

Once the stack is running, open a browser and go to:

```
https://<login>.42.fr
```

replacing `<login>` with the actual login configured for this project
(e.g. `https://mewaysi.42.fr`).

The browser will show a security warning the first time, because the site
uses a self-signed TLS certificate rather than one issued by a public
certificate authority — this is expected for this project. You can safely
proceed past the warning.

To reach the WordPress administration panel (for managing posts, users,
plugins, etc.):

```
https://<login>.42.fr/wp-admin
```

Log in there using the WordPress administrator account described below.

## Locating and managing credentials

All passwords for this stack are stored as individual files inside the
`secrets/` folder at the project root — never inside any configuration
file that gets shared or committed to version control.

| File | What it's for |
|---|---|
| `secrets/db_root_password.txt` | MariaDB root account password |
| `secrets/db_password.txt` | Password for the WordPress database administrator account |
| `secrets/db_password_2.txt` | Password for the second, regular database user account |

The WordPress site's own administrator login (used at `/wp-admin`) is
configured separately, through the `WORDPRESS_ADMIN_USER` and
`WORDPRESS_ADMIN_PASS` values in the `.env` file at the project root.

If you need to change any password, update the relevant file/variable and
restart the stack with `make re` so the change takes effect (existing data
is preserved; only the containers are rebuilt).

## Checking that the services are running correctly

To see the status of all three containers:

```bash
docker ps
```

All three (`nginx`, `wordpress`, `mariadb`) should show a status of `Up`. If
one instead shows `Restarting` or `Exited`, something has gone wrong —
check its logs for details:

```bash
docker logs nginx
docker logs wordpress
docker logs mariadb
```

If the website itself doesn't load in the browser but all three containers
show `Up`, double-check that `<login>.42.fr` actually resolves to the
virtual machine's IP address (this is usually configured through the
host machine's `/etc/hosts` file, not something the stack manages itself).
