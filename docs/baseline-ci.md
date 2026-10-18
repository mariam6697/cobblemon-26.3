# Fabric baseline CI

Issue: [#1](https://github.com/mariam6697/cobblemon-26.3/issues/1).
The reference target is Minecraft **1.21.1 / Java 21**. This check does not establish
Minecraft 26.3 compatibility or gameplay correctness.

## Workflow behavior

`.github/workflows/fabric-baseline.yml` runs on pull requests targeting `main`,
pushes to `main`, and manual dispatch. It uses Ubuntu 24.04 and Temurin Java 21.
The checkout, Java setup and artifact-upload actions are pinned to verified commit
revisions. The job uses read-only repository permissions.

The build step sets `GRADLE_USER_HOME` to a fresh directory under the runner's
temporary directory. It does not restore Gradle dependency/task caches. Kotlin
compiles in the Gradle process, with a 6 GiB heap, two workers and no parallel
project execution. The job timeout is 30 minutes.

With `JAVA_HOME` pointing to an existing JDK 21, the equivalent build command is:

```sh
GRADLE_USER_HOME=/path/to/new/empty/gradle-home ./gradlew \
  -Penabled_platforms=fabric \
  -Pkotlin.compiler.execution.strategy=in-process \
  -Dorg.gradle.jvmargs=-Xmx6G \
  --no-build-cache --no-parallel --max-workers=2 \
  :fabric:assemble --console=plain
python3 .github/scripts/verify_baseline.py
```

For a clean reproduction, run this from a fresh source checkout with no existing
`build/`, module build directories or `.gradle/` state. Use a new Gradle user home.
Running the command in a previously built checkout does not establish a clean build.

## Fixed build inputs

- Loom: `1.11.458`.
- Architectury Plugin: `3.4.164`.
- Gradle ZIP: `8.14.3`, with its [official SHA-256](https://services.gradle.org/distributions/gradle-8.14.3-bin.zip.sha256) in the wrapper properties.

These are the exact tool versions used by the earlier successful local reference;
this change replaces mutable snapshot coordinates without upgrading their resolved
versions. Java patch releases, runner images, network repositories and snapshot
build metadata can still vary. This check is not a bit-for-bit reproducibility guarantee.

## Artifact checks

`.github/scripts/verify_baseline.py` requires exactly one production Fabric JAR.
It verifies archive CRC integrity, the Cobblemon mod ID, Minecraft 1.21.1 / Java 21
metadata, Java 21 Pokémon bytecode, expected bootstrap/classes/resources, and
presence of every declared embedded dependency. It records the file size and SHA-256
in `build/reports/baseline-artifact.json`. This is packaging validation, not a client
or server gameplay test.

After verification, CI uploads the production JAR and report as
`fabric-baseline-1.21.1`, retained for seven days. Invalid artifacts fail the job;
they are not uploaded as verified builds.

## Clean local reproduction — 2026-10-18

A fresh checkout of merged source commit `5bd443f40e`, with the proposed CI
configuration applied, started without build outputs, project Gradle state or a
Gradle user home. No user-local Maven repository was present. It used Microsoft
OpenJDK 21.0.7 on macOS ARM64 and the build flags shown above.

Result: **BUILD SUCCESSFUL in 8m 39s**; all 30 actionable tasks executed, with no
build-cache hits. The production JAR passed the same verification command used by
CI, and its copied output matched the Fabric module artifact.

- Artifact: `build/libs/Cobblemon-fabric-1.8.3+1.21.1-fabric-baseline-5bd443f.jar`.
- Bytes: 151,257,221.
- SHA-256: `348076482a020dc25646295150ec62ae635d30db0b9e62c5211c54ec98ab1161`.
- Metadata: Minecraft `1.21.1`, Java `21`, Pokémon bytecode major `65`.
- Embedded dependency JARs: 8.

This validates a clean local build on macOS; it does not prove the Ubuntu hosted
job, Temurin setup or GitHub artifact upload have succeeded.

## Validation status

- Workflow: actionlint 1.7.12 passed locally; optional ShellCheck/Pyflakes integrations were unavailable and disabled.
- Verifier: accepted the previous and clean-build production JARs; rejected missing/invalid artifacts; accepted a dev-prefixed branch name while excluding source/Javadoc/development classifiers.
- Fresh-checkout build with an empty Gradle user home: passed locally on macOS ARM64 / JDK 21, as recorded above.
- Hosted Ubuntu job and artifact upload: not run yet; publication approval is required before pushing the workflow.

Keep issue #1 open until the hosted workflow has succeeded. Loader confirmation,
26.3 source migration and runtime tests remain separate roadmap tasks.
