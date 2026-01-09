#!/bin/bash
# Casino Production Server - Critical Security Remediation Script
# Server: 185.191.118.191
# Date: 2025-12-14
#
# IMPORTANT: Review each section before running!
# Run as root: bash remediation-critical.sh
#
set -e

echo "================================================"
echo "Casino Production Server - Security Remediation"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# Generate secure passwords
echo -e "${YELLOW}Generating secure passwords...${NC}"
POSTGRES_NEW_PASSWORD=$(openssl rand -base64 32 | tr -d '=+/')
REDIS_NEW_PASSWORD=$(openssl rand -base64 32 | tr -d '=+/')
JWT_NEW_SECRET=$(openssl rand -base64 64 | tr -d '\n')

echo "New passwords generated. Save these securely:"
echo "=========================================="
echo "POSTGRES_PASSWORD: $POSTGRES_NEW_PASSWORD"
echo "REDIS_PASSWORD: $REDIS_NEW_PASSWORD"
echo "JWT_SECRET: $JWT_NEW_SECRET"
echo "=========================================="
echo ""

read -p "Have you saved these passwords? (yes/no): " saved_passwords
if [ "$saved_passwords" != "yes" ]; then
    echo "Please save the passwords before continuing."
    exit 1
fi

# 1. FIREWALL SETUP
echo ""
echo -e "${GREEN}1. Configuring UFW Firewall...${NC}"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw --force enable
ufw status verbose

# 2. INSTALL FAIL2BAN
echo ""
echo -e "${GREEN}2. Installing and configuring Fail2Ban...${NC}"
apt update
apt install -y fail2ban

cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
ignoreip = 127.0.0.1/8 ::1

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600

[nginx-limit-req]
enabled = true
port = http,https
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
maxretry = 10
bantime = 3600
EOF

systemctl enable fail2ban
systemctl restart fail2ban
fail2ban-client status

# 3. SSH HARDENING
echo ""
echo -e "${GREEN}3. Hardening SSH configuration...${NC}"
echo -e "${YELLOW}WARNING: Ensure you have SSH key access before proceeding!${NC}"
read -p "Do you have SSH key access configured? (yes/no): " ssh_key_ready
if [ "$ssh_key_ready" = "yes" ]; then
    # Backup original config
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d)

    # Apply hardening
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
    sed -i 's/^#\?X11Forwarding.*/X11Forwarding no/' /etc/ssh/sshd_config

    # Validate and restart
    sshd -t && systemctl restart sshd
    echo "SSH hardened successfully"
else
    echo -e "${RED}Skipping SSH hardening - set up SSH keys first!${NC}"
fi

# 4. REDIS AUTHENTICATION
echo ""
echo -e "${GREEN}4. Configuring Redis authentication...${NC}"
cp /etc/redis/redis.conf /etc/redis/redis.conf.backup.$(date +%Y%m%d)
sed -i "s/^# requirepass.*/requirepass $REDIS_NEW_PASSWORD/" /etc/redis/redis.conf
sed -i "s/^requirepass.*/requirepass $REDIS_NEW_PASSWORD/" /etc/redis/redis.conf
sed -i 's/^protected-mode no/protected-mode yes/' /etc/redis/redis.conf
systemctl restart redis
echo "Redis authentication configured"

# 5. POSTGRESQL PASSWORD CHANGE
echo ""
echo -e "${GREEN}5. Changing PostgreSQL password...${NC}"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$POSTGRES_NEW_PASSWORD';"
echo "PostgreSQL password changed"

# 6. NGINX HARDENING
echo ""
echo -e "${GREEN}6. Hardening Nginx configuration...${NC}"
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.$(date +%Y%m%d)

# Enable server_tokens off
sed -i 's/# server_tokens off;/server_tokens off;/' /etc/nginx/nginx.conf

# Fix TLS protocols
sed -i 's/ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;/ssl_protocols TLSv1.2 TLSv1.3;/' /etc/nginx/nginx.conf

nginx -t && systemctl reload nginx
echo "Nginx hardened"

# 7. INSTALL CERTBOT FOR SSL
echo ""
echo -e "${GREEN}7. Installing Certbot for SSL...${NC}"
apt install -y certbot python3-certbot-nginx

echo ""
echo -e "${YELLOW}To obtain SSL certificate, run:${NC}"
echo "certbot --nginx -d api.betportal.com"
echo ""

# 8. DISABLE SMTP IF NOT NEEDED
echo ""
read -p "Do you need the mail server (Postfix) running? (yes/no): " need_mail
if [ "$need_mail" != "yes" ]; then
    echo -e "${GREEN}8. Disabling Postfix...${NC}"
    systemctl stop postfix
    systemctl disable postfix
    echo "Postfix disabled"
fi

# 9. CREATE BACKUP SCRIPTS
echo ""
echo -e "${GREEN}9. Setting up backup scripts...${NC}"
mkdir -p /var/backups/postgresql
mkdir -p /var/backups/redis

cat > /usr/local/bin/pg_backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/postgresql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U postgres -Fc casinocore > "$BACKUP_DIR/casinocore_$TIMESTAMP.dump"
find $BACKUP_DIR -name "*.dump" -mtime +7 -delete
echo "PostgreSQL backup completed: $TIMESTAMP"
EOF

cat > /usr/local/bin/redis_backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/redis"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
redis-cli BGSAVE
sleep 5
cp /var/lib/redis/dump.rdb "$BACKUP_DIR/dump_$TIMESTAMP.rdb"
find $BACKUP_DIR -name "*.rdb" -mtime +7 -delete
echo "Redis backup completed: $TIMESTAMP"
EOF

chmod +x /usr/local/bin/pg_backup.sh
chmod +x /usr/local/bin/redis_backup.sh

# Add to crontab
(crontab -l 2>/dev/null | grep -v "pg_backup\|redis_backup"; echo "0 2 * * * /usr/local/bin/pg_backup.sh >> /var/log/backup.log 2>&1"; echo "0 3 * * * /usr/local/bin/redis_backup.sh >> /var/log/backup.log 2>&1") | crontab -
echo "Backup scripts configured"

# 10. SYSTEM TUNING
echo ""
echo -e "${GREEN}10. Applying system tuning...${NC}"
cat > /etc/sysctl.d/99-casino-production.conf << 'EOF'
# Network optimization
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 65536
net.ipv4.tcp_max_syn_backlog = 65536
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_keepalive_time = 300

# Virtual memory
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5

# File descriptors
fs.file-max = 2097152

# Disable IPv6 if not used
# net.ipv6.conf.all.disable_ipv6 = 1
EOF

sysctl -p /etc/sysctl.d/99-casino-production.conf

# 11. CREATE SECURE ENV FILE FOR DOCKER
echo ""
echo -e "${GREEN}11. Creating secure environment file...${NC}"
cat > /root/.env.casino << EOF
# Casino Core Environment Variables
# Generated: $(date)
# DO NOT COMMIT TO VERSION CONTROL

# Database
POSTGRES_PASSWORD=$POSTGRES_NEW_PASSWORD
SPRING_DATASOURCE_PASSWORD=$POSTGRES_NEW_PASSWORD

# Redis
REDIS_PASSWORD=$REDIS_NEW_PASSWORD

# JWT
JWT_SECRET=$JWT_NEW_SECRET

# Add other secrets here
# OPERATOR_API_SECRETKEY=your-key
# PROVIDER_SECRET_KEY=your-key
EOF

chmod 600 /root/.env.casino
echo "Secure environment file created at /root/.env.casino"

echo ""
echo "================================================"
echo -e "${GREEN}Critical remediation completed!${NC}"
echo "================================================"
echo ""
echo "NEXT STEPS:"
echo "1. Update docker-compose.yml to use env_file: /root/.env.casino"
echo "2. Update application with new Redis password"
echo "3. Run: certbot --nginx -d api.betportal.com"
echo "4. Apply PostgreSQL tuning (see PRODUCTION_AUDIT_2025-12-14.md)"
echo "5. Restart the Docker container after updating credentials"
echo ""
echo -e "${YELLOW}IMPORTANT: Save your new credentials securely!${NC}"
echo ""
