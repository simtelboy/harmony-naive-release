# Atlantis Harmony release builder (public)

CI only; the HAP source stays in the private repository
`simtelboy/harmony-naive` and is checked out at build time.

## Required secrets

| Secret | Value |
|---|---|
| `PRIVATE_REPO_TOKEN` | Fine-grained PAT, **Contents: Read-only** on `simtelboy/harmony-naive` only |
| `SIGN_P12_PASS` | Password of the signing keystore used by `scripts/build-and-sign.sh` |

## Self-hosted runner

A HarmonyOS HAP needs the DevEco SDK, which GitHub-hosted runners do not have.
Register this PC as a self-hosted runner (Settings → Actions → Runners → New
self-hosted runner) and give it the extra label `harmony`:

```bash
./config.cmd --url https://github.com/simtelboy/harmony-naive-release --token <runner-token> --labels harmony
./run.cmd
```

Install it as a Windows service so the daily schedule works while logged out.
Signing materials are picked up from `C:\Worker\AGC通用证书` by the build script.

## Output

Each run builds a signed HAP and publishes a release named
`harmony-<versionName>-<versionCode>` for direct `hdc install`.
