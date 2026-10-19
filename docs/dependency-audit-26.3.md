# Minecraft 26.3 dependency audit

Checked on 2026-10-18 for [issue #2](https://github.com/mariam6697/cobblemon-26.3/issues/2),
against fork base `11536e3ebe740a717cb6be16eac83c366e46d0e5`.
This is a publication and source audit. No dependency, build script, server or
runtime behavior changes are included. Published candidates have not been
validated together in the full mod on Java 25.

## Loader decision remains open

The existing server loader has not been confirmed. Fabric remains a preliminary
development path, supported by the reference CI; it is not an approved deployment
decision. A vanilla server cannot load Cobblemon without a mod loader. Ask the
owner to confirm the existing setup and choose one initial port loader before
issue #3. Use a separate test server; preserve the active server and Minecraft 26.3.

## Build and required runtime matrix

Current versions come from `gradle/libs.versions.toml`, `gradle.properties`,
`gradle/build-logic/`, and the platform build scripts. A candidate is a starting
point for issue #3, not a change to the pinned 1.21.1 reference.

| Component | Current reference | 26.3 evidence / candidate | Proposed treatment and remaining validation |
| --- | --- | --- | --- |
| Minecraft / Java | 1.21.1 / 21 | Official 26.3 manifest requires Java 25 | Update together; preserve reference CI until a deliberate replacement. |
| Gradle | 8.14.3 | Fabric's 26.3 guidance specifies 9.6.0 | Update wrapper with official checksum; validate all build plugins. |
| Loom / Architectury Plugin | 1.11.458 / 3.4.164 | Architectury publishes Loom 1.17.493 and Plugin 3.5.170; its setup guide requires `dev.architectury.loom-no-remap` for 26.x | One viable build path. Compare with upstream NeoLoom before choosing; remove obsolete mappings/remap task assumptions coherently. |
| Kotlin compiler / stdlib / reflect | 2.2.20 | Maven Central publishes 2.4.21 for all three | Align compiler and runtime; test Java 25 target and build plugins. |
| Fabric Loader | 0.17.2 | Fabric's 26.3 endpoint marks 0.19.5 stable; 0.20.0 is not stable | If Fabric is chosen, start with stable 0.19.5; do not select the first response blindly. |
| Fabric API | 0.116.6+1.21.1 | Published 0.163.0+26.3 | If Fabric is chosen, port source calls to changed/removed APIs. Availability does not imply source compatibility. |
| Fabric Language Kotlin | 1.13.6+kotlin.2.2.20 | Published 1.14.2+kotlin.2.4.21 | If Fabric is chosen, align with Kotlin 2.4.21; audit nested JARs and runtime loading. |
| NeoForge | 21.1.195 | Published 26.3.0.92; Architectury documents minimum 26.3.0.48-beta | Alternative loader candidate, not an additional initial target. No full NeoForge build was tested. |
| Kotlin for Forge | 5.10.0 | Publisher's 26.3-filtered Modrinth listing advertises 6.4.0 for NeoForge; Maven metadata includes it | Needed if NeoForge is selected. Verify transitive Kotlin alignment and runtime loading. |
| MoLang | local.com.bedrockk:molang:1.1.20 | Vendored JAR and POM exist in `deps/local/com/bedrockk/molang/1.1.20/`; upstream's 26.1.2 branch retains it | Keep initially. Validate expressions/animation on Java 25; no Minecraft-specific publication is expected for this library. |
| Graal JS / SDK / regex / Truffle | 22.3.0 each | Existing POMs still available on Maven Central; upstream's 26.1.2 branch instead declares Graal 25.0.2 and additional modules | Required for the Graal Showdown implementation. Java 25 execution and packaging are unresolved; inspect upstream changes before deciding versions. A POM check does not validate a battle. |
| ICU4J | 71.1 | Existing POM available on Maven Central; upstream retains it alongside Graal's shadowed ICU | Audit duplication/relocation with Graal; test actual JS engine initialization. |
| MongoDB driver core / sync | 4.10.2 | Both POMs available on Maven Central; upstream retains these versions | Preserve persistence capability initially. Java 25 and Mongo-backed save/reload remain unverified. |
| Shadow / license / Blossom / IDEA plugins | 8.1.1 / 0.6.1 / 2.1.0 / 1.1.7 | Upstream changes Shadow to com.gradleup.shadow 9.3.2 and license plugin to net.neoforged.licenser 0.7.5 | These are build tools, not Minecraft runtime mods. Resolve and test under the selected Gradle path in #3; compatibility is not established here. |
| Test libraries | JUnit 5.11.4, Mockito 5.14.2, MockK 1.13.14, ClassGraph 4.8.179, Fabric Loader JUnit 0.17.2 | Existing baseline declarations; upstream changes JUnit to 6.0.3 | Reconcile with selected loader/toolchain in #3; no Java 25 test suite was run. |

`neoforge-moddev` 1.0.11 is declared in the catalog but not applied by the current
conventions; do not treat it as the active build path. Architectury **Plugin/Loom**
are build dependencies here; Architectury **API** is not currently a declared
runtime dependency and is not automatically required by this audit.

## Optional integrations and development mods

The following first-increment classifications are proposals awaiting confirmation.
All current dependencies and source registrations remain intact in this change.
Modrinth evidence below is filtered to `game_versions=["26.3"]`; versions are
publisher-advertised game compatibility, not a successful compilation of our API
usage. Maven API coordinates/classifiers still need resolution checks in #3.

| Integration | Current reference | Advertised 26.3 availability | Proposed first-increment scope / source coupling |
| --- | --- | --- | --- |
| JEI | 19.22.1.316 | 31.16.0.84 beta, Fabric and NeoForge | Defer recipe-viewer support. Common JEI plugin/categories, cooking-pot screen calls and an import in `BrewingStandRecipe.kt` must be reconciled; Fabric declares `jei_mod_plugin`. Removing only the dependency would break compilation. |
| Adorn | Modrinth version ID QbzMhTAO | No matching 26.3 versions returned | Defer furniture compatibility. Reconcile `AdornCompatibility.kt`, `AdornRegisterInvoker.java`, common mixin registration, item-group guard, resources and data packs together. Empty search results describe this source/date, not proof that no port exists anywhere. |
| AppleSkin | mc1.21-3.0.5 API classifier | 3.0.10+mc26.3 release, both loaders | Defer HUD integration. Fabric `appleskin` entrypoint and both platform handler classes need coordinated handling; NeoForge conditionally registers its handler. |
| LambDynamicLights | API 4.1.6+1.21.1, Mojmap capability | 4.13.0+26.3 release advertises Fabric, NeoForge and Quilt | Defer dynamic lighting. Common initializer/luminance classes and Fabric `dynamiclights` entrypoint depend on its API. The old `api-mojmap` capability must not be assumed valid for 26.3. |
| Mod Menu | 11.0.3 | 21.0.0 release, Fabric/Quilt | Defer config-menu integration. Fabric implementation dependency, `CobblemonModMenu.kt`, entrypoint and custom metadata require review. |
| Fabric Permissions API | 0.3.1 | 0.7.0 release advertises Fabric 26.3; Maven Central POM available | Prefer preserving command permission integration if Fabric is selected. It is optional at runtime: registration checks `fabric-permissions-api-v0`; `FabricPermissionValidator.kt` still requires its API at compile time. Test presence and absence. |
| C2ME | Fabric 0.3.0+alpha.0.320+1.21.1; NeoForge 0.3.0+alpha.0.73+1.21.1 | Fabric 0.4.2-alpha.0.106+26.3; NeoForge 0.4.2-alpha.0.105+26.3 | Defer performance testing until correctness is established. Currently development `modRuntimeOnly`; no direct source API imports found in the audited source roots. |
| Debug Utils | 1.21.1-1.0.9, loader-specific | 26.2-1.0.9-fabric / -neoforge are tagged compatible with 26.3 despite their version names | Opt-in development aid later. Currently `modLocalRuntime`; no direct source API imports found. Do not infer game compatibility from the filename alone. |

Deferral needs a separate implementation increment covering source references,
entrypoints, mixins and assets, followed by absent/present integration startup
checks. This audit does not authorize removing integrations or deleting saved
content. The default build still includes its original integrations.

## Reusable upstream work

After fetching upstream, all 223 fetched refs expose `mc_version` in
`gradle.properties`: 186 target 1.21.1, 31 target 1.20.1, four target 1.21,
one targets 1.19.2, and one targets **26.1.2** (the count includes `upstream/HEAD`).
No fetched ref declares 26.3. This does not cover unpublished work or merge requests
whose commits are not exposed by fetched branch refs.

- [main at f9dd1448e58ce69815aa759aae154b22a7fca025](https://gitlab.com/cable-mc/cobblemon/-/tree/f9dd1448e58ce69815aa759aae154b22a7fca025) still declares 1.21.1 / Java 21.
- [version/1.9 at 396ab13164d70ad5e7420c16001cef1f8199c61d](https://gitlab.com/cable-mc/cobblemon/-/tree/396ab13164d70ad5e7420c16001cef1f8199c61d) also declares 1.21.1 / Java 21.
- [feature/version-bump at 584983e6162f04b922ed0247e7327db561ba3fed](https://gitlab.com/cable-mc/cobblemon/-/tree/584983e6162f04b922ed0247e7327db561ba3fed) declares 26.1.2 / Java 25. It uses Gradle 9.4.0, Kotlin 2.3.20, `org.relativitymc.neo-loom` 1.16-SNAPSHOT, newer Shadow/license plugins, Graal 25.0.2 and revised packaging/Showdown code.

Review that last branch before independently rewriting the same systems. Its
aggregate diff from our merge base spans 4,064 files, including gameplay/assets;
do not equate the full branch with an isolated build patch. Commit messages claim
pipeline fixes, but neither its build nor its hosted pipeline was verified here.
Any selective reuse needs a separate reviewed increment, preserving attribution
and adapting further 26.3 API changes. Nothing was merged or cherry-picked.

## Next bounded step

Confirm the existing server setup and one initial loader, approve or revise the
integration scope, then compare the upstream build/Showdown changes with the
Architectury no-remap path. Split issue #3 before importing broad upstream changes.
Keep issue #2 open until the loader decision and dependency treatment are agreed.
The next build must report dependency resolution separately from compiler errors,
startup, persistence and battle results.

## Primary sources and verification limits

- [Official 26.3 manifest](https://piston-meta.mojang.com/v1/packages/11f1aefe473eefba0af62e3286c33b692807b2eb/26.3.json): Java runtime major 25.
- [Fabric 26.3 guidance](https://www.fabricmc.net/2026/09/15/263.html): Gradle/Loom/Loader guidance and API migration changes.
- [Architectury setup](https://github.com/architectury/architectury-docs/blob/main/docs/getting-started/setup.mdx): no-remap plugin and 26.3 prerequisites.
- [Fabric loader endpoint](https://meta.fabricmc.net/v2/versions/loader/26.3), [Fabric API metadata](https://maven.fabricmc.net/net/fabricmc/fabric-api/fabric-api/maven-metadata.xml), [Fabric Kotlin metadata](https://maven.fabricmc.net/net/fabricmc/fabric-language-kotlin/maven-metadata.xml).
- [Architectury Loom metadata](https://maven.architectury.dev/dev/architectury/architectury-loom/maven-metadata.xml), [Architectury Plugin metadata](https://maven.architectury.dev/architectury-plugin/architectury-plugin.gradle.plugin/maven-metadata.xml): versions are not sorted; candidates were selected by numeric suffix within the required line and their POMs checked.
- [NeoForge metadata](https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml), [Kotlin for Forge metadata](https://thedarkcolour.github.io/KotlinForForge/thedarkcolour/kotlinforforge-neoforge/maven-metadata.xml), [Kotlin for Forge 26.3 listing](https://api.modrinth.com/v2/project/kotlin-for-forge/version?game_versions=%5B%2226.3%22%5D).
- [Kotlin 2.4.21](https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-gradle-plugin/2.4.21/kotlin-gradle-plugin-2.4.21.pom), [Graal JS 22.3.0](https://repo.maven.apache.org/maven2/org/graalvm/js/js/22.3.0/js-22.3.0.pom), [MongoDB sync 4.10.2](https://repo.maven.apache.org/maven2/org/mongodb/mongodb-driver-sync/4.10.2/mongodb-driver-sync-4.10.2.pom), [Permissions 0.7.0](https://repo.maven.apache.org/maven2/me/lucko/fabric-permissions-api/0.7.0/fabric-permissions-api-0.7.0.pom): POM availability checked, including companion components listed in the matrix.
- Publisher listings queried through Modrinth's 26.3-filtered version API: [JEI](https://api.modrinth.com/v2/project/jei/version?game_versions=%5B%2226.3%22%5D), [Adorn](https://api.modrinth.com/v2/project/adorn/version?game_versions=%5B%2226.3%22%5D), [AppleSkin](https://api.modrinth.com/v2/project/appleskin/version?game_versions=%5B%2226.3%22%5D), [LambDynamicLights](https://api.modrinth.com/v2/project/lambdynamiclights/version?game_versions=%5B%2226.3%22%5D), [Mod Menu](https://api.modrinth.com/v2/project/modmenu/version?game_versions=%5B%2226.3%22%5D), [Permissions](https://api.modrinth.com/v2/project/fabric-permissions-api/version?game_versions=%5B%2226.3%22%5D), [C2ME Fabric](https://api.modrinth.com/v2/project/c2me-fabric/version?game_versions=%5B%2226.3%22%5D), [C2ME NeoForge](https://api.modrinth.com/v2/project/c2me-neoforge/version?game_versions=%5B%2226.3%22%5D), [Debug Utils](https://api.modrinth.com/v2/project/debugutils/version?game_versions=%5B%2226.3%22%5D).

No full-mod compilation, launch, gameplay, MongoDB or Showdown execution was
performed for this documentation increment. The successful baseline CI remains
Minecraft 1.21.1 / Java 21 and is not evidence of 26.3 runtime compatibility.
