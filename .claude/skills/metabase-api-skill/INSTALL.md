# Installation & Setup Guide

## Quick Start

### 1. Install the Skill

For Claude Code, copy this directory to your skills folder:

```bash
# On macOS/Linux
mkdir -p ~/.claude/skills/
cp -r metabase-api-skill ~/.claude/skills/

# Or add as a git submodule in your project
git submodule add <repo-url> skills/metabase-api
```

### 2. Install Python Dependencies

```bash
cd metabase-api-skill
pip install -r requirements.txt
```

Or use a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your Metabase credentials:

```env
METABASE_URL=https://your-metabase.com
METABASE_API_KEY=your-api-key
```

**Getting your API Key:**

Option 1 - Via Metabase UI (if available):
1. Go to Settings → Admin → API Keys
2. Create new API key
3. Copy the key

Option 2 - Using username/password:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "your@email.com", "password": "yourpass"}' \
  https://your-metabase.com/api/session
```

This returns a session token. Add to `.env`:
```env
METABASE_SESSION_TOKEN=the-token-from-response
```

### 4. Verify Installation

Test the connection:

```bash
python metabase_cli.py databases
```

You should see a list of available databases.

## Detailed Setup

### For Development

1. **Clone or download this skill:**
   ```bash
   git clone <repo-url> metabase-api-skill
   cd metabase-api-skill
   ```

2. **Set up Python environment:**
   ```bash
   # Using virtualenv
   python -m venv venv
   source venv/bin/activate
   
   # Or using conda
   conda create -n metabase python=3.9
   conda activate metabase
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure credentials:**
   ```bash
   # Copy template
   cp .env.example .env
   
   # Edit with your editor
   nano .env  # or vim, code, etc.
   ```

5. **Run examples:**
   ```bash
   python examples.py
   ```

### For Production/CI/CD

1. **Use environment variables directly:**
   ```bash
   export METABASE_URL="https://metabase.prod.com"
   export METABASE_API_KEY="prod-key"
   ```

2. **Or use secrets management:**
   - AWS Secrets Manager
   - HashiCorp Vault
   - Kubernetes Secrets
   - GitHub Secrets (for Actions)

3. **Install in CI pipeline:**
   ```yaml
   # .github/workflows/metabase.yml
   - name: Install Metabase skill
     run: |
       pip install -r metabase-api-skill/requirements.txt
   
   - name: Deploy queries to Metabase
     env:
       METABASE_URL: ${{ secrets.METABASE_URL }}
       METABASE_API_KEY: ${{ secrets.METABASE_API_KEY }}
     run: |
       python metabase-api-skill/metabase_cli.py import "queries/*.sql" -d 1
   ```

### For Docker

Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV METABASE_URL=""
ENV METABASE_API_KEY=""

CMD ["python", "examples.py"]
```

Build and run:

```bash
docker build -t metabase-skill .
docker run --env-file .env metabase-skill
```

## Troubleshooting

### Issue: Cannot connect to Metabase

**Check:**
1. Is `METABASE_URL` correct?
2. Can you access it in browser?
3. Is authentication configured?

**Test:**
```bash
curl -H "X-Api-Key: $METABASE_API_KEY" \
  $METABASE_URL/api/database/
```

### Issue: Session token expired

**Solution:**
Regenerate token or use API key instead.

```python
# Regenerate token
mb = MetabaseClient(
    base_url=url,
    username=user,
    password=pass
)
new_token = mb.session_token
```

### Issue: Import errors

**Check Python version:**
```bash
python --version  # Should be 3.7+
```

**Reinstall dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Permission denied

**Solution:**
Make scripts executable:
```bash
chmod +x metabase_cli.py metabase_helper.py examples.py
```

### Issue: SQL syntax error

**Solution:**
Test query first:
```bash
python metabase_cli.py query \
  --database-id 1 \
  --sql "YOUR_QUERY" \
  --show-results
```

## Verification Steps

Run these commands to verify everything works:

```bash
# 1. Check connection
python metabase_cli.py databases

# 2. List existing resources
python metabase_cli.py collections
python metabase_cli.py cards

# 3. Create a test card
python metabase_cli.py create "Test Card" \
  --database-id 1 \
  --sql "SELECT 1 as test"

# 4. Run examples
python examples.py

# 5. Use Python API
python -c "
from metabase_helper import MetabaseClient
import os
mb = MetabaseClient(
    base_url=os.getenv('METABASE_URL'),
    api_key=os.getenv('METABASE_API_KEY')
)
print('Connected! Found', len(mb.list_databases()), 'databases')
"
```

## Next Steps

After installation:

1. **Read the documentation:**
   - `SKILL.md` - Complete API reference
   - `README.md` - Usage examples
   - `CLAUDE.md` - Claude Code integration

2. **Run examples:**
   ```bash
   python examples.py
   ```

3. **Start using:**
   - Create your first card
   - Import SQL files
   - Organize into collections

4. **Integrate with Claude Code:**
   - Ask Claude to create Metabase cards
   - Automate query deployment
   - Manage analytics workflows

## Updating

To update the skill:

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

## Uninstalling

```bash
# Remove skill directory
rm -rf ~/.claude/skills/metabase-api-skill

# Deactivate virtual environment (if used)
deactivate

# Remove virtual environment
rm -rf venv
```

## Support

For issues or questions:
1. Check the documentation
2. Review examples
3. Test with CLI tool
4. Check Metabase API docs: `https://your-metabase.com/api/docs`
