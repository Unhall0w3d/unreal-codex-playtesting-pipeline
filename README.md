# Unreal + Codex Runtime Playtesting Pipeline

This is a sanitized, public-repository starter bundle for a Playwright-style
testing loop over a packaged Unreal Engine game. It was generalized from a
Linux/Unreal Engine 5.8.1 prototype.

The original material in this repository is available under the
[Apache License 2.0](LICENSE). See [THIRD_PARTY.md](THIRD_PARTY.md) before
copying, modifying, or redistributing an upstream dependency or any game
content.

Start with [Getting started for humans and Codex](docs/getting-started.md).
Then use [the engineering guide](docs/automated-unreal-codex-playtesting-pipeline.md)
for the full Unreal architecture and qualification model.

## Included

- `docs/automated-unreal-codex-playtesting-pipeline.md` — architecture,
  security boundaries, integration approach, and qualification matrix.
- `docs/getting-started.md` — clean-clone human setup, Codex orientation,
  first text-review run, and acceptance checklist.
- `docs/security-checklist.md` — pre-publication and runtime checks.
- `config/codex-config.toml.example` — generic project-scoped MCP config.
- `scripts/mcp-server.sh.example` — forced-loopback STDIO wrapper.
- `scripts/setup-dependency.sh.example` — checksum-pinned installer pattern.
- `scripts/run-smoke.sh.example` — bounded process lifecycle skeleton.
- `scripts/capture-hyprland-window.sh.example` — generic rendered-window
  capture adapter for Hyprland 0.55+.
- `scripts/local-review-openai.py` — bounded reference adapter for an
  interchangeable local text/image review worker.
- `contracts/` — closed task and result schemas for local review workers.
- `docs/local-model-workers.md` — capability, authority, qualification, and
  agentic expansion model for provider-neutral local workers.
- `scripts/mcp_driver.py` — dependency-free protocol/client skeleton.
- `examples/semantic-provider-contract.md` — game-side contract design.
- `THIRD_PARTY.md` — attribution and redistribution boundary.
- `AGENTS.md` and `examples/AGENTS.project-snippet.md` — Codex-readable
  repository and adopter-project authority boundaries.

## Important boundaries

This bundle does **not** contain an Unreal plugin, Unreal Engine, Epic/Fab
assets, the original game, third-party source, release binaries, credentials,
or private machine data. The scripts are reviewed templates and require
project-specific integration before they can control a game.

The tested third-party pins are historical qualification evidence. Revalidate
current upstream releases, checksums, compatibility, and licenses before use.

The Hyprland capture example is deliberately separate from semantic gameplay
tests. It uses a readiness log marker and a new-window address diff to capture
the exact rendered client geometry with `grim`; it does not inspect a DOM or
pretend that a native game is a browser. On Hyprland 0.56+, its optional narrow
initial-class rule places splash and replacement clients on a visible dedicated
workspace at map time without following focus, then disables itself during
cleanup. Render capture has its own hard timeout, and the resulting image still
requires manual review.

The local-worker extension is model-neutral. Qwen is one possible local
implementation, not a pipeline dependency. Workers advertise capabilities and
return provenance-bearing candidate evidence; they receive no code-mutation
authority, and orchestration and approval stay outside the model.

## Before using this as a project

Implement a distributable sample fixture, add CI, revalidate the current
dependency versions and checksums, then perform a clean-room install and
independent security review. Follow [SECURITY.md](SECURITY.md) for private
vulnerability reporting.
