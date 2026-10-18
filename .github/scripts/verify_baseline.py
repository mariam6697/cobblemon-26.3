#!/usr/bin/env python3
"""Check the packaged Fabric 1.21.1 reference, without starting Minecraft."""

import argparse
import hashlib
import json
from pathlib import Path
import zipfile


REQUIRED_ENTRIES = (
    "com/cobblemon/mod/fabric/FabricBootstrap.class",
    "com/cobblemon/mod/common/pokemon/Pokemon.class",
    "mixins.cobblemon-common.json",
    "mixins.cobblemon-fabric.json",
    "cobblemon-common.accesswidener",
    "assets/cobblemon/icon_cobblemon.png",
)


def verify(artifact_directory: Path) -> dict:
    artifacts = [
        path for path in artifact_directory.glob("Cobblemon-fabric-*.jar")
        if not path.name.endswith(("-sources.jar", "-javadoc.jar", "-dev-shadow.jar", "-dev-slim.jar"))
    ]
    if len(artifacts) != 1:
        raise ValueError(f"Expected one production JAR, found {len(artifacts)}")
    artifact = artifacts[0]

    with zipfile.ZipFile(artifact) as archive:
        bad_entry = archive.testzip()
        if bad_entry is not None:
            raise ValueError(f"Archive integrity failed: {bad_entry}")
        entries = set(archive.namelist())
        missing = set(REQUIRED_ENTRIES) - entries
        if missing:
            raise ValueError(f"Required entries are missing: {sorted(missing)}")
        metadata = json.loads(archive.read("fabric.mod.json"))
        dependencies = metadata["depends"]
        if metadata["id"] != "cobblemon":
            raise ValueError("The artifact is not Cobblemon")
        if dependencies["minecraft"] != "1.21.1" or dependencies["java"] != "21":
            raise ValueError("The reference must target Minecraft 1.21.1 and Java 21")
        pokemon = archive.read(REQUIRED_ENTRIES[1])
        if pokemon[:4] != b"\xca\xfe\xba\xbe" or int.from_bytes(pokemon[6:8], "big") != 65:
            raise ValueError("Pokémon bytecode must target Java 21 (class version 65)")
        embedded_jars = metadata.get("jars", [])
        if not embedded_jars:
            raise ValueError("No embedded runtime dependencies are declared")
        for embedded in embedded_jars:
            if embedded["file"] not in entries:
                raise ValueError(f"Embedded dependency is missing: {embedded['file']}")

    digest = hashlib.sha256()
    with artifact.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "artifact": str(artifact),
        "bytes": artifact.stat().st_size,
        "sha256": digest.hexdigest(),
        "mod_version": metadata["version"],
        "minecraft": dependencies["minecraft"],
        "java": dependencies["java"],
        "class_file_major": 65,
        "embedded_jars": len(embedded_jars),
        "archive_integrity": "passed",
        "required_entries": "passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", type=Path, default=Path("build/libs"))
    parser.add_argument("--output", type=Path, default=Path("build/reports/baseline-artifact.json"))
    args = parser.parse_args()
    try:
        report = verify(args.artifact_dir)
    except (ValueError, KeyError, OSError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Baseline artifact verification failed: {error}\n")
    rendered = json.dumps(report, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
