# Decision 0001: Develop the 26.3 port incrementally

Status: Accepted by the user on 2026-10-18.

## Decision

Keep Minecraft Java 26.3 as the final target. Use the open-source Cobblemon code
and host the fork on GitHub. Work across sessions, with one bounded issue or subtask
per session instead of attempting the entire port at once.

## Rationale

The codebase spans multiple subsystems and substantial Minecraft API changes.
Small, reviewable increments make validation and handoffs practical.

## Consequences

- Keep the imported upstream baseline on `main` and use a development branch.
- Validate the 1.21.1 baseline as a reference; this does not downgrade the active server.
- Track deliverables and acceptance criteria in GitHub issues.
- Split large issues after inspecting compiler errors.
- Keep agent plans and progress in ignored `.agent-work/` files, following the
  user's personal agent-config boilerplate adopted on 2026-10-18.
- Keep repository documentation in English; chat remains in Spanish.
- Present a concrete PR proposal and obtain approval before a new branch push
  or PR publication, including draft PRs.
- The server loader remains unresolved; no loader decision is implied by the
  preliminary Fabric checks.

See [the roadmap](../plan.md) and [requirements](../requirements/port-26.3.md).
