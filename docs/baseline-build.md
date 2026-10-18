# Fabric 1.21.1 baseline build

Verified on 2026-10-18 from source commit `e1a1faf8d6` on `port/26.3`.
This is a reference build of Cobblemon for Minecraft **1.21.1**, not a playable 26.3 port.

## Environment

| Component | Version |
| --- | --- |
| Minecraft | 1.21.1 |
| Java | Microsoft OpenJDK 21.0.7, macOS ARM64 |
| Gradle wrapper | 8.14.3 |
| Kotlin | 2.2.20 |
| Architectury Loom resolved snapshot | 1.11.458 |
| Architectury Plugin resolved snapshot | 3.4.164 |
| Fabric Loader | 0.17.2 |
| Fabric API | 0.116.6+1.21.1 |

Set `JAVA_HOME` to an existing JDK 21, then run from the repository root:

```sh
GRADLE_USER_HOME="$PWD/.gradle/user-home" ./gradlew -Penabled_platforms=fabric :fabric:assemble --console=plain
```

`enabled_platforms=fabric` selects Fabric and the common module. The existing
multi-loader default remains unchanged when the property is omitted. The local
cache and generated build outputs are ignored by Git.

## Result

The build completed with `BUILD SUCCESSFUL in 2m 38s`: 30 actionable tasks,
25 executed, 4 from cache and 1 up to date.

- Artifact: `build/libs/Cobblemon-fabric-1.8.3+1.21.1-26.3-e1a1faf.jar`.
- File size: 151,257,209 bytes.
- SHA-256: `ea0c797dac96014fc972ba794e703d047609a11413d46e6b104b43e341420337`.
- Archive CRC integrity: passed for every entry.
- Fabric metadata targets Minecraft `1.21.1` and Java `21`.
- Pokémon class bytecode major version: `65` (Java 21).
- Bootstrap, Pokémon class, both mixin configurations, access widener and icon: present.
- Archive entries: 42,862; embedded dependency JARs: 8.
- Copied output under `build/libs/` matches the artifact under `fabric/build/libs/`.

The `26.3` segment in this snapshot filename comes from the development branch
name. It does not change the Minecraft target declared in `fabric.mod.json`.
The exact artifact checksum applies to this build; snapshot filenames and build
metadata may change with subsequent commits.

## Warnings and limits

The build reports existing deprecations, Kotlin Java-nullability/type warnings,
missing Java annotation metadata, a mixin mapping warning, Javadoc warnings and
an ICU version-format warning. Gradle also reports deprecated features incompatible
with Gradle 9. These warnings did not stop the build; migration work remains separate.

This run used the preserved dependency cache and existing build outputs. A clean
installation and CI have not been validated, and snapshot plugin coordinates are
still mutable. Therefore this result is evidence of a successful local reference
build, not proof of clean-environment reproducibility.

No client startup, Pokémon capture, battle, persistence or dedicated-server
behavior has been tested. The user's active server was not changed.

## Follow-up

A later [clean local reproduction and CI configuration](baseline-ci.md) passed
with an empty dependency cache and no build-cache hits. That record also documents
the pinned tool versions. The cached run above remains a separate historical result.

Issue [#1](https://github.com/mariam6697/cobblemon-26.3/issues/1) remains open until
the hosted CI workflow succeeds. Document any platform/dependency issues before
starting the 26.3 source migration.
