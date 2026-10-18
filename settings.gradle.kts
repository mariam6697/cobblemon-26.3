enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()

        maven("https://maven.fabricmc.net/")
        maven("https://maven.architectury.dev/")
        maven("https://maven.minecraftforge.net/")
    }

    includeBuild("gradle/build-logic")
}

rootProject.name = "cobblemon"

val enabledPlatforms = providers.gradleProperty("enabled_platforms")
    .orElse("fabric,neoforge")
    .get()
    .split(',')
    .map(String::trim)
    .distinct()

require(enabledPlatforms.isNotEmpty() && enabledPlatforms.all { it in setOf("fabric", "neoforge") }) {
    "enabled_platforms must contain fabric, neoforge, or both (comma-separated)."
}

(listOf("common") + enabledPlatforms).forEach { setupProject(it, file(it)) }

fun setupProject(name: String, projectDirectory: File) = setupProject(name) {
    projectDir = projectDirectory
}

inline fun setupProject(name: String, block: ProjectDescriptor.() -> Unit) {
    include(name)
    project(":$name").apply(block)
}
