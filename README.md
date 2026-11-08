# .Staples. VRChat Tools

A shared VCC package catalog. Each tool keeps its own source repository and release downloads.
Adding this catalog does not install every package.

## Add to VCC

Open <https://vrc-staples.github.io/vpm-packages/> and select **Add to VCC**.

For manual setup, open **Settings > Packages** in VCC and add this repository URL:

```text
https://vrc-staples.github.io/vpm-packages/index.json
```

The catalog ID is `com.staples.vpm`. Keep this ID and the feed URL stable.

## Available packages

| Package | Version | Source |
| --- | --- | --- |
| Avatar Settings Manager - Lite | 1.1.0 | [AvatarSettingsManager-Lite](https://github.com/VRC-Staples/AvatarSettingsManager-Lite) |
| Avatar Settings Manager - Lite | 1.2.0-beta.2 (prerelease) | [AvatarSettingsManager-Lite](https://github.com/VRC-Staples/AvatarSettingsManager-Lite) |

ASM-Lite retains the package ID `com.staples.asm-lite` and its existing release downloads.
It requires Unity 2022.3, the VRChat Avatar SDK, and VRCFury.
The existing ASM-Lite-only catalog remains available and unchanged.

The maintenance prerelease is opt-in. Nightly builds are not listed.
The package's own license applies to its contents; this catalog does not relicense packages.

Before you install a prerelease, back up your Unity project.

1. In VCC, open **Settings > Packages**.
2. Enable **Show Pre-Release Packages**.
3. Open your project's package list and select `1.2.0-beta.2` for ASM-Lite.

## Update the catalog

New releases use `.Staples. - <Tool Name>` in the package manifest and catalog entry's `displayName`.
Keep website labels and machine-readable package `name` IDs unchanged.
Preserve existing release ZIPs. For older releases, apply the prefix to catalog metadata only.

1. Publish an approved, versioned package ZIP in the tool's own repository.
2. Copy its root `package.json` into the matching entry in `docs/index.json`.
   Apply the VCC display-name prefix above.
3. Add its fixed release download URL and the ZIP's SHA-256 as `zipSHA256`.
4. Update the package information in `docs/index.html` and run the check below.
5. Commit and push the reviewed changes to `main` to publish through GitHub Pages.

Do not point version entries at overwritable `nightly` or `latest` downloads.
Do not change existing package IDs to rename the catalog.
Before merging maintenance into main, set the package manifest to the approved stable version.
After the stable release is published, add its versioned ZIP to this catalog.

```sh
python -m unittest discover -s tests
```

The publishing workflow runs these checks before deployment. They check the listing and install
link, not execution in Unity or VCC. Verify new release downloads and their hashes before publishing.
The website uses plain HTML links and local CSS, with no JavaScript or external UI dependencies.
