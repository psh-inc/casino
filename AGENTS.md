# AGENTS.md - Agent Instructions for Monorepo

This document contains instructions for AI agents working on the casino monorepo.

## Monorepo Architecture

The project uses **Git submodules** to manage three independent repositories:

| Repo | Remote | Purpose | Location |
|------|--------|---------|----------|
| `casino-b/` | `git@github.com:psh-inc/core.git` | Backend (Kotlin/Spring Boot 3.2.5) | `casino-b/` |
| `casino-f/` | `git@github.com:psh-inc/cadmin.git` | Admin Frontend (Angular 17) | `casino-f/` |
| `casino-customer-f/` | `git@github.com:psh-inc/casino-customer-f.git` | Customer Frontend (Angular 17) | `casino-customer-f/` |

Each repository maintains:
- ✅ Its own git history and branches
- ✅ Its own remote origin
- ✅ Independent development and release cycles
- ✅ Separate CI/CD pipelines

The **root monorepo** serves as an orchestration point, tracking all submodules at specific commit references.

## Working with Submodules

### Clone the Monorepo

```bash
# Fresh clone with all submodules
git clone --recurse-submodules <root-repo-url>

# Or if already cloned without submodules
git submodule update --init --recursive
```

### Check Submodule Status

```bash
# View current commit of each submodule
git submodule status

# Expected output:
# 1c8e3163d8ba9f1ef19e302dddde232d6f98e0ab casino-b (heads/master)
# 0ad358e7394dc24e5172eb1423316b95457a9d2d casino-customer-f (heads/master)
# 26b2df19752807bbe47d603d8ef90629785eef8d casino-f (heads/master)
```

### Push Changes to a Submodule

```bash
# Make changes in a submodule
cd casino-b
git add .
git commit -m "[Backend] New feature description

Your detailed explanation here.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
git push origin master

# Return to root and update the submodule reference
cd ..
git add casino-b                          # Stage the submodule commit change
git commit -m "[Infra] Update casino-b submodule

Update casino-b to latest master branch.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
git push                                  # Push root monorepo changes
```

### Pull Latest from All Submodules

```bash
# Update all submodules to their latest remote commits
git submodule update --remote

# Then commit the changes in root
git add casino-b casino-f casino-customer-f
git commit -m "[Infra] Update all submodules to latest"
git push
```

## Critical Rules for Agents

1. **Always work within submodule directories**: Don't modify files outside their respective repos
2. **Push to submodule remotes first**: Changes to a submodule must be pushed to its own origin
3. **Then update root repo**: After pushing submodule changes, update and push the root monorepo
4. **Never force-push to master**: Use `git push --force` only if explicitly authorized
5. **Keep submodule references in sync**: Before major operations, run `git submodule update --remote`
6. **Verify builds before submitting**:
   - Backend: `cd casino-b && ./gradlew clean build`
   - Admin Frontend: `cd casino-f && npm install && ng build`
   - Customer Frontend: `cd casino-customer-f && npm install && ng build`

## Commit Conventions

Use the format below for all commits:

```
[Component] Brief description

Longer explanation if needed.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

### Component Prefixes

- **Backend**: `[Backend]`, `[Auth]`, `[Player]`, `[Game]`, `[Bonus]`, `[Wallet]`, `[Sports]`, `[KYC]`, `[DB]`, `[Kafka]`, `[Cache]`
- **Admin Frontend**: `[Admin]`, `[UI]`, `[Forms]`, `[Reports]`
- **Customer Frontend**: `[Frontend]`, `[Games]`, `[Account]`, `[Wallet]`, `[Promotions]`, `[Sports]`
- **Infra**: `[Infra]`, `[CI/CD]`, `[Docker]`, `[Deploy]`
- **Fix**: `[Fix]`, `[Refactor]`, `[Perf]`

## Task Workflow

When assigned a task:

1. **Identify scope**: Determine which submodule(s) are affected
2. **Plan changes**: Read CLAUDE.md for critical rules and patterns
3. **Implement**: Make changes, test thoroughly
4. **Verify builds**: Ensure no build failures
5. **Commit**: Use proper commit message format
6. **Push twice**:
   - Push submodule changes to its remote
   - Push root repo with updated submodule reference
7. **Update task status**: Move task from "todo" to "ready for testing" in Jira

## Useful Commands

```bash
# View git log for submodule
cd casino-b && git log --oneline -10 && cd ..

# See what changed in submodule since last update
git submodule summary

# Clone fresh with all history
git clone --recurse-submodules --depth=1 <root-repo-url>

# Update all submodules to remote main/master
git submodule foreach git pull origin master

# Check if any submodule has uncommitted changes
git status  # Look for "modified: casino-b" etc
```

## Troubleshooting

### Submodule is in detached HEAD state

```bash
cd casino-b
git checkout master
git pull origin master
cd ..
git add casino-b
git commit -m "[Infra] Update casino-b to master"
```

### Submodule changes not showing up

```bash
# Ensure you're in the submodule directory
cd casino-b
git status        # Should show your changes

# If not, check your working directory
pwd               # Should be .../casino-b/
```

### "already exists" error when adding submodule

This means a submodule is partially configured. Remove and re-add:

```bash
git rm --cached casino-b
rm -rf casino-b/.git
git submodule add git@github.com:psh-inc/core.git casino-b
```

## Architecture Reference

See [CLAUDE.md](./CLAUDE.md) for:
- Complete project structure
- Technology stack and versions
- Code patterns and conventions
- Database guidelines
- API standards
- Security rules
- Testing requirements
- Environment variables

---

**Last Updated**: 2025-01-10
**Monorepo Configured**: 2025-01-10
