# Minecraft Java 26.3 port roadmap

This is an unofficial port of [Cobblemon](https://gitlab.com/cable-mc/cobblemon).
The project will be developed incrementally across sessions. The final Minecraft
version remains 26.3; the loader for the existing server is not yet confirmed.
Fabric has only been used for preliminary development checks.

## Requirements and decisions

- [Port requirements and acceptance criteria](requirements/port-26.3.md)
- [Incremental development decision](decisions/0001-incremental-port.md)
- [Technical migration notes](porting-26.3.md)
- [26.3 dependency audit and open loader decision](dependency-audit-26.3.md)

## Work packages

| Issue | Deliverable | Dependencies |
| --- | --- | --- |
| [#1](https://github.com/mariam6697/cobblemon-26.3/issues/1) | Reproducible baseline build and CI | None |
| [#2](https://github.com/mariam6697/cobblemon-26.3/issues/2) | Confirm server loader and audit dependencies | None |
| [#3](https://github.com/mariam6697/cobblemon-26.3/issues/3) | Migrate build tooling to 26.3 and inventory compiler errors | #1, #2 |
| [#4](https://github.com/mariam6697/cobblemon-26.3/issues/4) | Port entities, registries and serialization | #3 |
| [#5](https://github.com/mariam6697/cobblemon-26.3/issues/5) | Port blocks, components and world generation | #3 |
| [#6](https://github.com/mariam6697/cobblemon-26.3/issues/6) | Render a Pokémon and port client interfaces | #4 |
| [#7](https://github.com/mariam6697/cobblemon-26.3/issues/7) | Capture, party, PC storage and persistence | #4, #5, #6 |
| [#8](https://github.com/mariam6697/cobblemon-26.3/issues/8) | Complete a Showdown battle | #7 |
| [#9](https://github.com/mariam6697/cobblemon-26.3/issues/9) | Dedicated-server validation and experimental release | #5, #6, #7, #8 |

Each issue defines acceptance criteria. Split work packages into smaller issues
when the compiler inventory establishes their actual scope. Effort estimates
remain provisional until that inventory exists.

GitHub issues hold delivery status. Local implementation plans and session
progress belong in ignored `.agent-work/<feature-slug>/` files, not this roadmap.
