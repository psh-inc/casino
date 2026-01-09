# Host Filesystem Layout + Kernel/Limits Tuning (185.191.118.191)

**Host:** `185.191.118.191` (`capable-goose`)  
**Last updated (UTC):** 2025-12-14  

## Filesystem layout

### Goal
Keep the OS root filesystem small and stable, and place mutable/high-churn data (Docker + PostgreSQL) on a dedicated data volume.

### Current state
- Root filesystem: `/dev/md0` (RAID1), ext4, mounted at `/` (~99 GiB)
- Data filesystem: `/dev/md1` (RAID1), ext4, mounted at `/srv` (~780 GiB), `noatime`
- Bind mounts:
  - `/srv/docker` → `/var/lib/docker`
  - `/srv/postgresql` → `/var/lib/postgresql`

### Safety copies (pre-cutover)
- `/var/lib/docker.bak_20251214T100110Z`
- `/var/lib/postgresql.bak_20251214T100110Z`

### Verification
- `df -hT / /srv /var/lib/docker /var/lib/postgresql`
- `findmnt -T /srv && findmnt -T /var/lib/docker && findmnt -T /var/lib/postgresql`
- `cat /proc/mdstat` (RAID resync/health)

## Kernel tuning (sysctl)

### Applied config
Host sysctl file: `/etc/sysctl.d/99-casino-performance.conf`
- `vm.swappiness = 10`
- Dirty writeback smoothing:
  - `vm.dirty_background_ratio = 5`
  - `vm.dirty_ratio = 15`
  - `vm.dirty_expire_centisecs = 3000`
  - `vm.dirty_writeback_centisecs = 500`
- Network backlog:
  - `net.core.somaxconn = 65535`
  - `net.ipv4.tcp_max_syn_backlog = 65535`
  - `net.core.netdev_max_backlog = 65536`
- Ephemeral ports:
  - `net.ipv4.ip_local_port_range = 10240 65535`

### Apply / check
- Apply: `sysctl --system`
- Check: `sysctl vm.swappiness vm.dirty_ratio net.core.somaxconn net.ipv4.ip_local_port_range`

## Service limits (systemd)

### Applied config
- Docker drop-in: `/etc/systemd/system/docker.service.d/99-limits.conf`
- PostgreSQL template drop-in: `/etc/systemd/system/postgresql@.service.d/99-limits.conf`

Both set:
- `LimitNOFILE=1048576`

### Apply / check
- Apply: `systemctl daemon-reload && systemctl restart postgresql docker`
- Check: `systemctl show docker -p LimitNOFILE && systemctl show postgresql@17-main -p LimitNOFILE`

## Rollback (if needed)

### Bind mounts rollback
1) `systemctl stop docker postgresql`
2) Remove the two bind-mount lines from `/etc/fstab`
3) `umount /var/lib/docker /var/lib/postgresql`
4) Restore: `mv /var/lib/docker.bak_* /var/lib/docker` and `mv /var/lib/postgresql.bak_* /var/lib/postgresql`
5) `systemctl start postgresql docker`

### Sysctl rollback
1) Remove or adjust `/etc/sysctl.d/99-casino-performance.conf`
2) `sysctl --system`

### Limits rollback
1) Remove the drop-ins under `/etc/systemd/system/*/99-limits.conf`
2) `systemctl daemon-reload && systemctl restart postgresql docker`

