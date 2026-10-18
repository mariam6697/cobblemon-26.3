# Minecraft Java 26.3 port requirements

## Goal

Run Cobblemon on Minecraft Java 26.3 while preserving core Pokémon behavior and
player data. Do not downgrade the user's existing server. Preserve upstream
attribution and the MPL-2.0 license and identify the fork as unofficial.

## First playable increment

A compatible client must open a disposable world, render a Pokémon, capture it,
place it in the party or PC, save, restart, and recover the same Pokémon with its
identity, owner, species, level and moves intact. A full battle must complete and
persist its results. Repeat core checks against a dedicated server with two clients.

## Delivery acceptance

- The baseline build is reproducible and recorded before migration.
- The selected loader and required dependencies resolve for 26.3.
- CI produces the experimental artifact and records actual validation outcomes.
- Generation, capture, storage, combat, reconnect and restart checks pass without
  lost or duplicated Pokémon on the documented test setup.
- Installation requirements, known limitations and untested scenarios are explicit.
- Tests run in disposable worlds and separate test servers; deployment to the
  user's active server requires separate authorization.

## Unresolved questions

- Existing server loader: vanilla, Fabric or NeoForge.
- Which optional integrations are included in the first release.
- Scope and effort of each migration work package after the compiler inventory.

Fabric is a preliminary development choice, not a confirmed user requirement.
See [the roadmap](../plan.md) for issue links and dependencies.
