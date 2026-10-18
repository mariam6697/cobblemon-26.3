# Port to Minecraft Java 26.3

This is an experimental community port, not an official Cobblemon release.
No playable 26.3 build has been validated. Do not install development builds on a live world.

The session-by-session roadmap and GitHub issues are in [the plan](plan.md).

## Starting point

- Upstream: https://gitlab.com/cable-mc/cobblemon
- Base commit: `b1066671f5c574cade74fc5af7b64e62cd7764c5`
- Upstream version: `1.8.3`, snapshot, Minecraft `1.21.1`, Java `21`.
- Migration branch: `port/26.3`.
- Initial scope: one loader and the common module; the server loader still needs confirmation.
- Source inventory: 2,969 common files (256,960 lines), 23 Fabric files (1,748 lines),
  21 NeoForge files (1,900 lines), counting `.kt` and `.java` under `src/main`.

The objective is to keep Minecraft 26.3 and port Cobblemon to it. Downgrading the
existing server is outside the scope of this project. Adding Cobblemon still
requires a compatible mod loader on the server and matching client installations.

## Verified target metadata

Checked on 2026-10-18 against Mojang and Fabric Maven metadata:

| Component | Upstream | Target / available version |
| --- | --- | --- |
| Minecraft | 1.21.1 | 26.3 |
| Java | 21 | 25 (`java-runtime-epsilon`) |
| Gradle | 8.14.3 | 9.6.0 recommended by Fabric's 26.3 announcement |
| Loom | Architectury 1.11-SNAPSHOT | 1.17.493 passed an isolated no-remap probe; full mod unverified |
| Fabric Loader | 0.17.2 | 0.19.5 stable |
| Fabric API | 0.116.6+1.21.1 | 0.163.0+26.3 published |

Available artifacts are not proof that Cobblemon or its build plugins work with them.

Sources:

- [Mojang version manifest](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json)
- [Fabric loader metadata for 26.3](https://meta.fabricmc.net/v2/versions/loader/26.3)
- [Fabric API Maven metadata](https://maven.fabricmc.net/net/fabricmc/fabric-api/fabric-api/maven-metadata.xml)
- [Fabric's 26.3 migration notes](https://www.fabricmc.net/2026/09/15/263.html)

## Milestones

- [x] Preserve upstream history, license and credits in GitHub.
- [x] Create the migration branch.
- [x] Verify official 26.3 runtime and loader metadata.
- [x] Compile the 1.21.1 reference with the preparatory changes (local cached build).
- [ ] Configure the selected loader and common module for 26.3 / Java 25.
- [ ] Resolve dependencies and produce a compiler error inventory.
- [ ] Compile the common and loader modules.
- [ ] Start a development client and open a disposable world.
- [ ] Spawn and render a Pokémon.
- [ ] Capture, save, restart, and recover that Pokémon.
- [ ] Complete a battle.
- [ ] Repeat capture, persistence, and battle checks on a dedicated server.

## Confirmed migration touchpoints

These are source references, not yet fixes or a complete inventory:

| Area | Existing usage | Migration work |
| --- | --- | --- |
| Build | Java target now comes from `java_version` | Verified build conventions compile; full-mod migration pending |
| Mappings | Mojang + Parchment 1.21 mappings in build conventions | Adapt to the unobfuscated 26.x toolchain |
| Composting | `CompostingChanceRegistry` in `CobblemonFabric.kt` | Migrate to item components |
| Stripping logs | `StrippableBlockRegistry` in `CobblemonFabric.kt` | Migrate to block transformers |
| Text input | Enter constants now use `InputConstants` | New input event signatures and text focus handling still need migration |
| World generation | Existing configured features and configurations | Audit against 26.3 feature registry and data changes |
| Rendering | Custom Pokémon rendering and client mixins | Audit against accumulated renderer changes since 1.21.1 |

Optional integrations (JEI, Adorn, AppleSkin, dynamic lights, Mod Menu, C2ME and
debug utilities) need their own compatibility audit. Removing a dependency without
also addressing its source references and entrypoints is not a valid migration.

## Baseline command

Use a JDK 21, then run from the repository root:

```sh
./gradlew -Penabled_platforms=fabric :fabric:assemble --console=plain
```

This selects only Fabric and the common module. Without `enabled_platforms`, the
build still includes Fabric and NeoForge. To reuse the downloaded local cache,
set `GRADLE_USER_HOME` to the absolute path of `.gradle/user-home` in this checkout.
It does not prove gameplay correctness or compatibility with 26.3.

## Validation record

- Build-convention compilation with Java 21: passed.
- Standalone 26.3 API probe with Java 25 / Gradle 9.6.0 / Architectury Loom 1.17.493:
  passed. Kotlin plugin 2.4.21, Fabric Loader 0.19.5 and Fabric API 0.163.0+26.3 resolved.
- Fabric 1.21.1 reference build: passed locally on 2026-10-18. See [build evidence and limits](baseline-build.md).
- Clean-install reproducibility and CI: not validated yet; issue #1 remains open.
- Full Cobblemon compilation against Minecraft 26.3: not attempted yet.
- Client and dedicated server gameplay: not attempted yet.
- Diagnostic logs retained locally in `.ignored/porting-logs/` (not versioned).
