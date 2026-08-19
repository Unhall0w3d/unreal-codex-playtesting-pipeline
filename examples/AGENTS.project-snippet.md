## Local playtest review worker

The project may use the vendored Unreal/Codex pipeline to delegate bounded
evidence review to a local model.

- Read the pipeline's `docs/getting-started.md` and
  `docs/local-model-workers.md` before use.
- Use only project-approved, qualified worker profiles.
- Require every mission capability explicitly and reject unsupported tasks.
- Keep endpoints numeric-loopback only and evidence under the approved ignored
  evidence root.
- Treat worker output as candidate evidence, not approval or ground truth.
- Never give the worker shell, credentials, arbitrary file access, source
  mutation, Git, game-process ownership, or autonomous repair authority.
- Codex or the human operator owns mission construction, process lifecycle,
  result verification, code changes, and final approval.
