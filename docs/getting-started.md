# Getting started: humans and Codex

This guide takes a fresh clone to the first bounded local-model review. The
repository supplies contracts, reference adapters, and integration patterns;
it does not bundle Unreal Engine, an Unreal plugin, an inference runtime, a
model, or game content.

## 1. Clone and inspect

```bash
git clone https://github.com/Unhall0w3d/unreal-codex-playtesting-pipeline.git
cd unreal-codex-playtesting-pipeline
python3 scripts/local-review-openai.py capabilities
python3 -m unittest discover -s tests -v
sha256sum -c SHA256SUMS
```

Prerequisites for the local-worker path are Python 3.10 or newer and a local
inference server with an OpenAI-compatible `/v1/chat/completions` endpoint.
The reference adapter uses only Python's standard library. Unreal integration
has separate engine, compiler, packaging, and plugin requirements described in
the [engineering guide](automated-unreal-codex-playtesting-pipeline.md).

Do not run downloaded installers or adopt the historical dependency pins until
you have independently reviewed the current release, checksum, and license.

## 2. Start a local inference server

Start the runtime you already trust with an explicitly selected model. Bind it
to an exact numeric loopback address such as `127.0.0.1`; do not expose an
unauthenticated review endpoint to the LAN. Confirm that its model identifier
and endpoint match the values you will pass to the adapter.

The server's model list proves only that an artifact is loaded. It does not
prove text-review quality, vision support, structured-output reliability, or
safe coexistence with a running game. Record those as qualification evidence
for the exact model, runtime, inference profile, and hardware tuple.

## 3. Run the included text-review example

With a compatible server listening locally, run:

```bash
python3 scripts/local-review-openai.py run \
  --request examples/local-text-review-task.json \
  --evidence-root examples \
  --endpoint http://127.0.0.1:8080/v1/chat/completions \
  --model your-local-model
```

Change the port and model alias to match your server. The command prints one
schema-validated provenance envelope. A successful request does not qualify
the model; it only proves basic protocol compatibility.

The example is intentionally text-only. Do not submit a `visual_review` task
unless the exact worker profile has qualified both `input.image` and
`review.visual`.

## 4. Integrate it into a game project

Copy or vendor the pipeline into the game repository, then:

1. put captured evidence in an ignored, project-owned directory;
2. create project-specific task manifests from the schemas in `contracts/`;
3. keep every evidence path relative to the single `--evidence-root`;
4. add the relevant section from `examples/AGENTS.project-snippet.md` to the
   game's own `AGENTS.md`;
5. run the adapter from a human- or Codex-owned orchestration step; and
6. validate the result and retain the approval decision outside the worker.

The local reviewer is a subprocess-style collaborator, not a native Codex
subagent. Codex prepares a bounded mission, runs the adapter, receives the
closed result, and decides what—if anything—should happen next. The model has
no Codex tools and no authority to edit code.

Unreal runtime control is a separate MCP integration. Review
`config/codex-config.toml.example`, copy only the relevant section into the
game's project-scoped `.codex/config.toml`, replace every placeholder, and
review the tool approval modes. The local review adapter itself does not need
an MCP entry.

## 5. Point Codex at the repository

For a local clone, open the repository or game project in Codex and use a
bounded request such as:

> Read AGENTS.md and docs/getting-started.md. Audit this machine and project
> for the text-review worker prerequisites. Do not install, download, start,
> or modify anything. Report the exact integration steps and blockers.

After human review, a second request can authorize the integration:

> Integrate the review-only local worker using the project AGENTS.md policy.
> Keep the endpoint on numeric loopback, use ignored evidence paths, run the
> included tests, and do not give the worker code or Git authority.

When providing only the GitHub URL, ask Codex to inspect the repository's
`README.md`, `AGENTS.md`, and this guide before proposing changes. A URL alone
does not install the pipeline or authorize repository mutation.

## 6. Acceptance checklist

Before relying on any result, verify:

- repository tests and checksum verification pass;
- the endpoint is numeric-loopback only;
- the mission declares only capabilities the exact profile has qualified;
- evidence stays below the configured size/count bounds and under its root;
- the worker receives no credentials, tools, source-write, shell, or Git
  access;
- malformed or contradictory results fail closed;
- game/model concurrent resource use is measured on the target machine; and
- a human or primary orchestrator retains the final decision.

Continue with [local-model workers](local-model-workers.md), the
[security checklist](security-checklist.md), and the
[engineering guide](automated-unreal-codex-playtesting-pipeline.md).
