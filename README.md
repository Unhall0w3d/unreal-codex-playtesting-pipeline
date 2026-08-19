# Unreal + Codex Runtime Playtesting Pipeline

This is a sanitized, public-repository starter bundle for a Playwright-style
testing loop over a packaged Unreal Engine game. It was generalized from a
Linux/Unreal Engine 5.8.1 prototype.

The original material in this repository is available under the
[Apache License 2.0](LICENSE). See [THIRD_PARTY.md](THIRD_PARTY.md) before
copying, modifying, or redistributing an upstream dependency or any game
content.

Start with [the engineering guide](docs/automated-unreal-codex-playtesting-pipeline.md).

## Included

- `docs/automated-unreal-codex-playtesting-pipeline.md` — architecture,
  security boundaries, integration approach, and qualification matrix.
- `docs/security-checklist.md` — pre-publication and runtime checks.
- `config/codex-config.toml.example` — generic project-scoped MCP config.
- `scripts/mcp-server.sh.example` — forced-loopback STDIO wrapper.
- `scripts/setup-dependency.sh.example` — checksum-pinned installer pattern.
- `scripts/run-smoke.sh.example` — bounded process lifecycle skeleton.
- `scripts/mcp_driver.py` — dependency-free protocol/client skeleton.
- `examples/semantic-provider-contract.md` — game-side contract design.
- `THIRD_PARTY.md` — attribution and redistribution boundary.

## Important boundaries

This bundle does **not** contain an Unreal plugin, Unreal Engine, Epic/Fab
assets, the original game, third-party source, release binaries, credentials,
or private machine data. The scripts are reviewed templates and require
project-specific integration before they can control a game.

The tested third-party pins are historical qualification evidence. Revalidate
current upstream releases, checksums, compatibility, and licenses before use.

## Before using this as a project

Implement a distributable sample fixture, add CI, revalidate the current
dependency versions and checksums, then perform a clean-room install and
independent security review. Follow [SECURITY.md](SECURITY.md) for private
vulnerability reporting.
