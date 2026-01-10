# Documentation Style Guide - Casino Platform

## Principles

- Use clear, testable language with SHALL/SHOULD/MAY when specifying behavior.
- Keep content tied to code. Avoid guesses; explicitly state when something is not defined in code.
- Avoid secrets and environment values in docs. Use variable names only.
- Prefer relative links to repo files.

## Formatting

- Headings are short and descriptive.
- Use lists for requirements and decisions.
- Use tables for configuration and interface summaries.
- Use Mermaid for diagrams when useful.

## Naming conventions

- Product name: "Casino Platform"
- Backend: casino-b
- Admin frontend: casino-f
- Customer frontend: casino-customer-f
- Shared library: casino-shared

## Normative language

- SHALL: required behavior
- SHOULD: recommended behavior
- MAY: optional behavior

## Links

- Use relative links to repo files when possible.
- Link to code directories for detailed implementation.
- Keep links stable; prefer README-level anchors.

## Quality bar

A document is "Approved" only when:
- Requirements are testable and unambiguous.
- Terminology is consistent with code.
- Failure modes and recovery steps are documented.
- Ownership and review cadence are explicit.
- No broken repo-local links.
