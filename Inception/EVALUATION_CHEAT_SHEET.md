# 42 Inception — Evaluation Cheat Sheet & Hard Questions

---

### Question 1: Linux Kernel Architecture
**"You say containers aren't virtual machines. What specific Linux kernel mechanisms make a container possible, and what does each one do?"**

**The Golden Answer:**
A container is just a regular Linux process on the host kernel, restricted by two primary kernel features and two filesystem features:
1. **Namespaces (Isolation):** Determines *what the process can see*.
   - `PID namespace`: The process sees itself as PID 1 inside the container, while having a normal PID (e.g., 24510) on the host.
   - `NET namespace`: Gives the container its own virtual network interfaces, routing tables, and port space.
   - `MNT namespace`: Isolates filesystem mount points.
   - `IPC & UTS namespaces`: Isolates inter-process shared memory and hostname.
2. **Cgroups (Control Groups - Resource Limits):** Determines *how much the process can use*. It caps and measures CPU time, RAM usage, and disk I/O so one container cannot starve the host.
3. **chroot / pivot_root & OverlayFS:** Switches the process's apparent root directory (`/`) to the image's filesystem and uses layered Copy-on-Write storage.

---

### Question 2: Docker Network & Internal DNS
**"In Nginx's configuration, you wrote `fastcgi_pass wordpress:9000;`. How does Nginx resolve `wordpress` to an IP, and how does the packet physically travel between the two containers?"**

**The Golden Answer:**
1. **DNS Resolution:**
   Docker runs an embedded DNS server inside the network namespace at IP `127.0.0.11`. When Nginx asks to resolve the hostname `wordpress`, the query hits `127.0.0.11`, which checks Docker’s internal service table and returns the container's private IP on `inception_net` (e.g., `172.19.0.3`).
2. **Packet Travel:**
   Each container has a virtual Ethernet interface (`eth0`) connected to a virtual peer interface (`veth...`) on the host. Both peers plug into a Linux software bridge (`br-...`). The packet leaves Nginx's `eth0`, passes through the bridge, and is forwarded directly to the WordPress container's `veth` interface via Layer-2 MAC routing on the host kernel.

---

### Question 3: The Volume Trick in Compose
**"In your `docker-compose.yml`, why did you declare volumes using `driver_opts: type: none, o: bind, device: /home/mewaysi/data/...` instead of just writing `- /home/mewaysi/data/wordpress:/var/www/wordpress` under the service?"**

**The Golden Answer:**
The short syntax (`./data:/var/www`) is a simple **bind mount**, directly managed at the container level.  
By defining it in the top-level `volumes:` section using the `local` driver with `o: bind`, Docker registers it as a **first-class Docker Named Volume**, while anchoring its storage backend to the exact directory required by the 42 subject (`/home/<login>/data`).  
This gives us the best of both worlds:
1. It satisfies the 42 subject requirement that data must persist in `/home/<login>/data`.
2. It lets other containers share the exact same volume by name (`wordpress_data`) rather than hardcoding file paths across multiple services.

---

### Question 4: The FastCGI / Nginx Shared Volume Dilemma
**"Why does NGINX need access to the WordPress files volume (`wordpress_data:/var/www/wordpress:ro`), if WordPress already has its own container?"**

**The Golden Answer:**
Because of how the FastCGI protocol and web servers work:
1. **Static Files:** Static assets (CSS, JS, images, `.html`) are served directly by Nginx for speed and security. Nginx needs to read them from disk without bothering PHP-FPM.
2. **FastCGI Script Passing:** When a `.php` file is requested, NGINX first uses `try_files $uri =404;` to verify that the `.php` file actually exists on disk before dispatching it. If it exists, Nginx sends FastCGI parameters (`SCRIPT_FILENAME /var/www/wordpress/index.php`) over the TCP socket to PHP-FPM.
If Nginx didn't have the volume mounted, it would return a `404 Not Found` before the request could ever reach PHP-FPM.

---

### Question 5: Database Bootstrapping & Security
**"Look at your MariaDB `entrypoint.sh`. Why did you start mysqld in the background with `--skip-networking --socket=...` during the initial setup, instead of just running it normally?"**

**The Golden Answer:**
When initializing a brand-new database with `mysql_install_db`, the `root` user temporarily has no password.
If we started MariaDB with standard networking enabled on port 3306, the database would be vulnerable to unauthenticated connections over the Docker bridge network before the password could be configured.
By passing `--skip-networking --socket=/run/mysqld/mysqld.sock`:
1. TCP networking is completely disabled; nobody can connect over the network.
2. We bootstrap the database, set the root password, create the database and users securely through the local UNIX domain socket.
3. We shut it down and cleanly restart MariaDB with normal networking via `exec mysqld`.

---

### Question 6: Zombie Processes and Signal Propagation
**"What happens under the hood when I run `docker stop mariadb`? Why did you use `exec mysqld` at the end of `entrypoint.sh`?"**

**The Golden Answer:**
When you run `docker stop`, Docker sends a `SIGTERM` signal to **PID 1** inside the container, giving it a 10-second grace period to shut down gracefully before sending `SIGKILL`.
If you run a shell script without `exec`:
- `/bin/bash` stays PID 1, and `mysqld` becomes a child process (PID 2).
- Bash does NOT forward `SIGTERM` to child processes by default.
- As a result, MariaDB never receives `SIGTERM`, does not flush dirty InnoDB buffer pool pages to disk, and gets forcefully terminated by `SIGKILL` 10 seconds later, risking table corruption.
Using `exec mysqld` causes the MariaDB binary to **replace** the shell process in memory while retaining PID 1. It receives `SIGTERM` directly, flushes all pending transactions, writes its log sequence numbers, and exits cleanly.

---

### Question 7: Docker Secrets vs Environment Variables
**"How does Docker Secrets physically work on Linux, and why is it superior to passing passwords via `environment:` in docker-compose?"**

**The Golden Answer:**
Environment variables have severe security weaknesses:
1. They are visible in cleartext to anyone with read access to Docker via `docker inspect <container>`.
2. They are inherited by all child processes and fork calls.
3. They frequently leak into crash reports, debugging dumps, and `/proc/<pid>/environ`.

In contrast, Docker Compose Secrets mounts each secret file into the container at `/run/secrets/<secret_name>` using **`tmpfs` (temporary in-memory filesystem)**. 
- The secret exists strictly in RAM and is never written to disk or baked into the image layers.
- When the container stops, the tmpfs mount disappears from memory.

---

### Question 8: TLS Handshake & Port 443
**"When I connect with `curl -k https://mewaysi.42.fr`, explain the TLS handshake that occurs between my client and Nginx."**

**The Golden Answer:**
1. **Client Hello:** The client sends supported TLS versions (TLS 1.2 / 1.3), supported cipher suites, and the SNI (*Server Name Indication* = `mewaysi.42.fr`).
2. **Server Hello & Certificate:** Nginx responds choosing TLS 1.3 and sends its public X.509 certificate containing its public RSA key.
3. **Key Exchange (Asymmetric):** The client and Nginx perform a Diffie-Hellman / ECDHE key exchange to securely compute a shared symmetric session key without transmitting it over the wire.
4. **Session Encryption (Symmetric):** Once the handshake finishes, all subsequent HTTP traffic (the GET request, WordPress HTML, cookies) is encrypted symmetrically using high-speed AES-GCM encryption with that session key.
