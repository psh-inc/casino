# AI Agent Implementation Plan - Casino Platform

## Purpose

Provide a repeatable workflow for AI-assisted changes in this repo.

## Required entry points

- AGENTS.md (submodule workflow rules)
- CLAUDE.md (architecture + coding rules)
- docs/03-modules/README.md (module boundaries)
- specs/README.md (contracts)

## Standard workflow

1) Identify scope
- Determine affected submodule(s): casino-b, casino-f, casino-customer-f, casino-shared
- Avoid cross-submodule edits unless required

2) Read relevant docs and code
- Use module specs under docs/03-modules
- For backend changes, review specs/openapi and specs/asyncapi

3) Implement changes
- Follow coding standards in CLAUDE.md
- Avoid introducing new features outside task scope

4) Update docs and specs
- Update docs for any behavior change
- Update specs for API/event changes

5) Validate
- Backend: ./gradlew clean build
- Admin frontend: npm install && ng build
- Customer frontend: npm install && ng build

6) Commit and push (submodule workflow)
- Commit and push inside the submodule first
- Update root submodule reference and commit

## Definition of done

- Code compiled and tests passed
- Docs/specs updated
- Link checks passed (scripts/check_md_links.py)
- Security and privacy concerns reviewed
