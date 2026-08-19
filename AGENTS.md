# Codex orientation

This repository is a public reference implementation for bounded Unreal Engine
runtime testing and local-model evidence review. It is not a turnkey Unreal
plugin and does not grant an AI model general control of a game or repository.

When a user asks you to install, evaluate, or integrate this repository:

1. Read `docs/getting-started.md` first.
2. Read `docs/local-model-workers.md` before using a local model.
3. Treat `contracts/` as the stable worker boundary and the scripts as
   reference adapters that require project-specific paths and review.
4. Keep all MCP and local-model endpoints numeric-loopback only.
5. Keep local-model workers review-only: no shell, source mutation, Git,
   credentials, arbitrary paths, or autonomous repair.
6. Reject a task when the selected, qualified worker profile does not satisfy
   every declared `required_capabilities` entry.
7. Treat every worker result as untrusted candidate evidence until the
   qualification policy permits narrower audit sampling.
8. Preserve human approval for code changes, security decisions, publication,
   and subjective visual or gameplay judgment.

Do not claim that cloning this repository automatically installs Unreal
support, an MCP server, a local inference runtime, or a model. Report those as
separate prerequisites and follow the clean-room checklist in the getting
started guide.
