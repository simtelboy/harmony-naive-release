# Atlantis Harmony release builder (public)

CI only; the HAP source stays in the private repository
`simtelboy/harmony-naive` and is checked out at build time.

It uses the community HarmonyOS CI container
`ghcr.io/dalongzhuazi/harmonyos-ci:api24`, which contains the OpenHarmony
command-line tools for API 24 (6.1.1) — the same image the private repo's own
workflow uses. GitHub-hosted runners do not ship the HarmonyOS SDK, so the
container is what makes an Actions-only build possible.

## Required secrets

| Secret | Value |
|---|---|
| `PRIVATE_REPO_TOKEN` | Fine-grained PAT, **Contents: Read-only** on `simtelboy/harmony-naive` only |
| `SIGNING_CERT` | base64 of the `.cer` |
| `SIGNING_PROFILE` | base64 of the `.p7b` |
| `SIGNING_KEY` | base64 of the `.p12` |
| `SIGNING_KEY_ALIAS` | keystore alias |
| `KEYSTORE_PASSWORD` | keystore password |
| `KEY_PASSWORD` | key password |

The same signing values are already used by the private repo's `Build HAP`
workflow; copy them here so the public builder can sign without access to the
private repository's secrets.

## Output

Each run builds a signed HAP and publishes a release named
`harmony-<versionName>-<versionCode>` for direct `hdc install`.
