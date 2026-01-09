# Production Audit & Hardening Recommendations

**Target:** `185.191.118.191` (`capable-goose`)  
**Date (UTC):** 2025-12-14  
**Scope:** Host OS, SSH, firewall, Nginx, Docker runtime + `casino-core` container, PostgreSQL, Redis  
**Method:** Initially read-only inspection via SSH; remediation was applied later (see **Remediation Status (Applied on Host)**).

---

## Current Topology (Observed)

`Cloudflare (api.betportal.com)` → `Nginx (host, :80)` → `casino-core (Docker, host network, :8080)` → `PostgreSQL (host, 127.0.0.1:5432)` + `Redis (host, 127.0.0.1:6379)`

> DNS for `api.betportal.com` resolves to Cloudflare IPs. Without an origin firewall allowlist, attackers can bypass Cloudflare/WAF by hitting the origin IP directly.

---

## Inventory Snapshot (Observed)

- **OS:** Ubuntu 24.04.3 LTS (Noble)
- **Kernel:** 6.14.0-33-generic
- **CPU/RAM:** 32 vCPU / 186 GiB RAM
- **Disk:** `/` is ~99 GiB on RAID1 (`/dev/md0`)  
  - Note: NVMe devices are ~894 GiB each. At audit time only ~101 GiB partitions were used in RAID for `/`. Additional capacity was later allocated to a new RAID1 data volume at `/srv` (details below).
- **Docker:** 29.1.x; Compose plugin installed
- **Nginx:** 1.24.0
- **PostgreSQL:** 17.7 (PGDG)
- **Redis:** 7.0.15

---

## Remediation Status (Applied on Host)

This section tracks concrete remediation that was later applied on `capable-goose` after the original audit snapshot (date/time is from host UTC).

### Network exposure / edge hardening
- **Firewall:** UFW enabled with default-deny inbound; allows `22/tcp` and allowlists `80/tcp` + `443/tcp` to Cloudflare IP ranges only.
- **Brute-force protection:** Fail2ban enabled (sshd jail), with active bans visible in `ufw status`.
- **Backend bypass:** `casino-core` no longer uses host networking; it is published on `127.0.0.1:8080` only (not publicly reachable).

### Logging / runtime safety
- **Persistent logs:** journald persistence enabled (`/var/log/journal`).
- **Docker log rotation:** Docker daemon configured for `json-file` rotation; `live-restore=true` enabled to reduce disruption during daemon restarts.

### Observability
- **Metrics stack (local-only):** Prometheus + exporters bound to `127.0.0.1` (node_exporter, postgres_exporter, blackbox exporter); Alertmanager running as `prometheus-alertmanager`.

### Host filesystem layout (data volume)
- **New RAID1 volume:** Created `/dev/md1` from unused NVMe space and mounted as ext4 at `/srv` with `noatime`.
- **Data relocated to `/srv`:**
  - `/var/lib/docker` is bind-mounted from `/srv/docker`
  - `/var/lib/postgresql` is bind-mounted from `/srv/postgresql`
- **Safety copies:** Pre-cutover originals are preserved on `/` as:
  - `/var/lib/docker.bak_20251214T100110Z`
  - `/var/lib/postgresql.bak_20251214T100110Z`

### App networking (Docker ↔ host services)
- **`casino-core` container:** runs on Docker `bridge` network (not `--network host`) with `-p 127.0.0.1:8080:8080`.
- **PostgreSQL reachability from container:** PostgreSQL listens on `localhost` + `172.17.0.1` (docker0) and `pg_hba.conf` allows `172.17.0.0/16` with `scram-sha-256`.
- **Redis reachability from container:** Redis listens on `127.0.0.1` + `172.17.0.1` (docker0); UFW allows container-to-host access on docker0.
- **UFW local rules:** `5432/tcp` and `6379/tcp` are allowed **only** on `docker0` from `172.17.0.0/16`.

### Nginx upstream
- **Local upstream:** Nginx `proxy_pass` uses `http://127.0.0.1:8080` (avoids `localhost` resolving to `::1` while Docker publishes IPv4 loopback).

### Kernel / limits tuning
- **Sysctl:** `/etc/sysctl.d/99-casino-performance.conf` applies conservative tuning for swappiness, dirty writeback, and network backlogs.
- **Systemd limits:** Drop-ins set `LimitNOFILE=1048576` for Docker and all `postgresql@*.service` units.

### Reduce unused services
- Masked/stopped: `sensu-client`, `apport`, `ModemManager`, `openvswitch-switch`, `multipathd` (+ socket), `open-iscsi`, `open-vm-tools`.

### Quick verification commands
- Storage: `df -hT / /srv /var/lib/docker /var/lib/postgresql`
- Mounts: `findmnt /srv /var/lib/docker /var/lib/postgresql`
- RAID: `cat /proc/mdstat`
- Sysctl: `sysctl vm.swappiness vm.dirty_ratio net.core.somaxconn`
- Limits: `systemctl show docker -p LimitNOFILE && systemctl show postgresql@17-main -p LimitNOFILE`

### Rollback (if needed)
1) Stop services: `systemctl stop docker postgresql`
2) Remove the two bind-mount lines from `/etc/fstab`
3) `umount /var/lib/docker /var/lib/postgresql`
4) Restore directories: `mv /var/lib/docker.bak_* /var/lib/docker` and `mv /var/lib/postgresql.bak_* /var/lib/postgresql`
5) Start services: `systemctl start postgresql docker`

## What’s Good Already

- **OS patching:** `unattended-upgrades` is enabled and active.
- **DB surface area:** PostgreSQL and Redis are bound to loopback only (not internet-facing).
- **Docker access:** `docker` group has no members (reduces lateral privilege escalation risk).
- **Container user:** `casino-core` runs as a non-root user (`appuser`).

---

## External Exposure (Verified)

### Listening ports (host)
- **Open to internet:** `22/tcp` (SSH), `80/tcp` (HTTP), `8080/tcp` (backend)  
- **Not present:** `443/tcp` (HTTPS not enabled on origin)
- **Local-only:** `5432/tcp` (PostgreSQL), `6379/tcp` (Redis)

**Critical note:** `8080/tcp` is reachable from the public internet and bypasses Nginx/Cloudflare controls.

---

## Findings (Prioritized)

Severity legend: **CRITICAL** = immediate exploitation risk / major blast radius, **HIGH** = significant risk, **MEDIUM** = hardening/operational maturity.

### CRITICAL-01 — Host firewall is disabled
**Evidence:** `ufw status` → inactive  
**Impact:** Origin is reachable directly on any listening service (including `:8080`).  
**Recommendation:** Enable a default-deny firewall and explicitly allow only required inbound sources/ports (see Remediation Plan).

---

### CRITICAL-02 — SSH allows root login and password authentication
**Evidence (effective config):** `PermitRootLogin yes`, `PasswordAuthentication yes`, `X11Forwarding yes`, `AllowTcpForwarding yes`  
**Impact:** High brute-force and credential stuffing risk; root is the most targeted account.  
**Recommendation:** Disable root SSH login, disable password auth, restrict users, disable X11 + TCP forwarding, reduce auth attempts, optionally add 2FA.

---

### CRITICAL-03 — Backend port `8080` is internet-accessible (bypasses Nginx/Cloudflare)
**Evidence:** `ss` shows `0.0.0.0:8080` listening; external connect to `185.191.118.191:8080` succeeds  
**Impact:** Bypasses WAF/rate limits, exposes actuator/health endpoints, increases attack surface and exploitability.  
**Recommendation (choose one):**
1) **Best:** Move container off host networking and publish `127.0.0.1:8080` only.  
2) **Fastest:** Keep host networking but bind the app to loopback (`server.address=127.0.0.1`).  
3) **Defense-in-depth:** Firewall deny inbound to `8080/tcp` regardless.

---

### CRITICAL-04 — Origin has no TLS (`443` not enabled)
**Evidence:** No process listening on `:443`; Certbot not installed; Nginx has only port `80` vhost(s).  
**Impact:** If Cloudflare is configured in “Flexible”/HTTP-to-origin mode, traffic between Cloudflare and origin is plaintext. Direct-to-origin access is also plaintext.  
**Recommendation:** Enable origin TLS and set Cloudflare to **Full (strict)**. Use Let’s Encrypt or Cloudflare Origin Certificates.

---

### CRITICAL-05 — Database credentials are weak / default (and app uses `postgres` superuser)
**Evidence (container env check, value not printed):**
- `POSTGRES_PASSWORD` and `SPRING_DATASOURCE_PASSWORD` match a common default string (very weak)
- App connects as `POSTGRES_USER=postgres`
**Impact:** If an attacker gains app env access (logs, docker access, RCE), DB compromise is immediate; using superuser increases blast radius.  
**Recommendation:**
- Rotate the database password immediately.
- Create a dedicated DB role for the app with least privilege (no superuser, no createdb/createrole).
- Keep `postgres` superuser for admin-only access via local peer auth.

---

### CRITICAL-06 — Redis has no authentication and protected-mode is disabled
**Evidence:** `protected-mode no`; no `requirepass`; `redis-cli PING` works without auth.  
**Impact:** Local compromise leads to immediate data tampering / cache poisoning / session takeover; risk increases if Redis ever becomes reachable beyond loopback (misconfig, SSRF, future changes).  
**Recommendation:** Enable ACL and require authentication; enable `protected-mode yes`; consider disabling/renaming dangerous commands.

---

### HIGH-01 — Nginx config loads a backup vhost, creating duplicate `server` blocks
**Evidence:** `/etc/nginx/sites-enabled/api.betportal.com.bak` exists and is included by wildcard.  
**Impact:** Undefined/fragile routing behavior, hard-to-debug production issues, and potential security misroutes.  
**Recommendation:** Remove the `.bak` file from `sites-enabled/` (keep backups outside included paths).

---

### HIGH-02 — Nginx leaks version in `Server` header
**Evidence:** Responses include `Server: nginx/1.24.0 (Ubuntu)`; `server_tokens off;` is commented out.  
**Impact:** Improves attacker reconnaissance and exploit targeting.  
**Recommendation:** Enable `server_tokens off;` and consider further header normalization at the edge (Cloudflare) if desired.

---

### HIGH-03 — No intrusion prevention (Fail2ban/sshguard)
**Evidence:** `fail2ban` not installed/running.  
**Impact:** No automated protection against brute-force attempts (especially harmful with password auth enabled).  
**Recommendation:** Install `fail2ban` (or `sshguard`) with `sshd` + `nginx` jails.

---

### HIGH-04 — Secrets are injected via container environment variables
**Evidence:** Container env contains secret-like variables (`*_PASSWORD`, `*_SECRET*`, `JWT_SECRET`)  
**Impact:** Any actor with Docker access can read secrets; accidental log/diagnostic capture risk; rotation discipline tends to degrade.  
**Recommendation:** Move secrets to a root-owned `env_file` (`chmod 600`) at minimum; ideally use Docker secrets or a secrets manager (Vault/SSM/etc). Rotate operator/provider keys regularly.

---

### HIGH-05 — No automated backups detected for PostgreSQL / Redis
**Evidence:** No root crontab; no backup jobs in `/etc/cron.d`; no DB backup directories beyond system backups.  
**Impact:** High risk of irreversible data loss (operator error, corruption, ransomware).  
**Recommendation:** Implement daily `pg_dump` + offsite copy (encrypted) and routinely test restores. Decide whether Redis persistence is required (cache vs state).

---

### MEDIUM-01 — Journald is not persistent
**Evidence:** `/var/log/journal` missing.  
**Impact:** Reduced incident response capability; logs lost after reboot; easier for attackers to cover tracks.  
**Recommendation:** Enable persistent journaling with sane retention limits.

---

### MEDIUM-02 — Docker log rotation not configured
**Evidence:** Docker uses `json-file` logging; no log-opts configured.  
**Impact:** Containers can fill `/` quickly with logs (root FS is ~99 GiB).  
**Recommendation:** Set `log-opts` (`max-size`, `max-file`) globally in `/etc/docker/daemon.json` or per container.

---

### MEDIUM-03 — Memory tuning needs revisiting for real workload
**Evidence:**
- `casino-core` container uses ~19 GiB RAM at steady state
- PostgreSQL is heavily provisioned vs current DB size (~69 MiB)
**Impact:** Not an immediate security issue, but affects efficiency and headroom planning.  
**Recommendation:** Add observability, set explicit container resource limits, and tune JVM/Postgres based on measured load (not just “server has lots of RAM”).

---

### MEDIUM-04 — Swappiness is default (`60`)
**Evidence:** `vm.swappiness = 60`  
**Impact:** Under memory pressure, the kernel may swap more aggressively than ideal for latency-sensitive services.  
**Recommendation:** Consider lowering to ~`10` for a DB/API host after validating memory behavior.

---

## Remediation Plan (Safe Order)

### Phase 0 (Immediate: 0–2 hours)
1) **Establish safe access**
   - Confirm SSH key auth works for `ubuntu` in a second session before changing SSH settings.
2) **Block direct backend access**
   - Quick mitigation: firewall deny inbound `8080/tcp`
   - Proper fix: bind backend to loopback or publish only to `127.0.0.1`
3) **Remove duplicate Nginx config**
   - Remove `sites-enabled/api.betportal.com.bak` from included path
4) **Rotate weak database password**
   - Update app config; restart app; verify DB connectivity

### Phase 1 (Today: 2–8 hours)
5) **Enable firewall (default deny)**
   - Allow SSH from admin IPs
   - Allow HTTP/HTTPS only from Cloudflare IP ranges
6) **Harden SSH**
   - Disable root login + password auth
   - Disable X11 forwarding and TCP forwarding (unless explicitly needed)
7) **Enable origin TLS**
   - Use Let’s Encrypt or Cloudflare Origin Cert
   - Set Cloudflare SSL mode to **Full (strict)**

### Phase 2 (This week)
8) **Install and configure Fail2ban**
9) **Add backups + offsite retention**
10) **Enable persistent logs + docker log rotation**
11) **Add Cloudflare real-IP handling in Nginx**
12) **Secure Redis (ACL + protected-mode)**

### Phase 3 (Next 1–4 weeks)
13) **Container hardening + deployment hygiene**
   - Move from ad-hoc `docker run` to `docker compose` (or systemd unit) with:
     - healthchecks
     - resource limits
     - `no-new-privileges`, `read_only`, dropped capabilities
14) **Observability**
   - Metrics (node_exporter, postgres_exporter, redis_exporter), logs, alerts
15) **PostgreSQL performance tooling**
   - Enable `pg_stat_statements`, slow query logging, and periodic review

---

## Concrete Recommendations (Implementation Notes)

### Firewall (UFW) — origin allowlisting for Cloudflare
Because `api.betportal.com` is behind Cloudflare, strongly consider:
- **Allow 80/443 only from Cloudflare IP ranges**
- **Block all other inbound to 80/443**
- Keep SSH restricted to your admin IPs/VPN

Cloudflare publishes canonical IP lists:
- IPv4: https://www.cloudflare.com/ips-v4
- IPv6: https://www.cloudflare.com/ips-v6

### SSH hardening checklist (OpenSSH best practices)
- `PermitRootLogin no` (or `prohibit-password`)
- `PasswordAuthentication no`
- `KbdInteractiveAuthentication no`
- `PubkeyAuthentication yes`
- `AllowUsers ubuntu` (or a dedicated ops user)
- `X11Forwarding no`
- `AllowTcpForwarding no` (unless required)
- `MaxAuthTries 3`
- Consider 2FA (e.g., `libpam-google-authenticator`) for interactive access

### Nginx behind Cloudflare
- Configure `real_ip_header CF-Connecting-IP;` and `set_real_ip_from` for Cloudflare IP ranges (only safe if you firewall allowlist Cloudflare).
- Add rate limiting at Nginx (and/or Cloudflare WAF rules).
- Remove `localhost` origins from CORS lists in production.
- Lock down `/actuator/**` and `/swagger-ui/**` (internal-only or authenticated).

### Docker container hardening (`casino-core`)
Target runtime flags (or compose equivalents):
- Avoid `--network host`; instead publish `127.0.0.1:8080:8080`
- `--security-opt no-new-privileges:true`
- `--read-only` with `--tmpfs /tmp:rw,nosuid,nodev,noexec,mode=1777`
- `--cap-drop=ALL`
- `--pids-limit=512` (tune as needed)
- `--memory`/`--cpus` limits to prevent noisy-neighbor and runaway JVM
- Add a healthcheck and wire it into restart/alerting

### PostgreSQL hardening
- Rotate app password; create least-privilege role for the app.
- Enable `pg_stat_statements` (requires `shared_preload_libraries`) for query visibility.
- Set up daily `pg_dump` + offsite backup; optionally WAL archiving for PITR.
- Plan storage: `/` is only ~99 GiB. Consider a dedicated RAID/LV mount for `/var/lib/postgresql` and `/var/lib/docker`.

### Redis hardening
- Enable `protected-mode yes`
- Require authentication (ACL-based is preferred)
- Set `maxmemory` and an eviction policy if Redis is used as a cache

---

## Suggested Reference Standards (Industry)

- **CIS Benchmarks:** Ubuntu Linux, Docker
- **OWASP:** ASVS + Cheat Sheets (deployment & secrets handling)
- **Mozilla SSL Configuration Generator:** https://ssl-config.mozilla.org/
- **Cloudflare Origin Security:** IP allowlisting + Full (strict) TLS
- **PostgreSQL docs:** security + runtime configuration guidance
- **Redis docs:** security guidance and ACLs

---

## Repo Templates

The `infra/` folder contains draft templates you can adapt:
- `infra/docker-compose.production.yml`
- `infra/nginx-api.betportal.com.conf`
- `infra/postgresql-production.conf`

Before applying templates on the server, review them against your actual deployment constraints and validate in staging.
