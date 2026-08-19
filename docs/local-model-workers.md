# Interchangeable local review workers

For fresh-clone installation, a runnable text example, and Codex prompts, begin
with [Getting started for humans and Codex](getting-started.md).

This extension lets an orchestrator delegate bounded evidence review to a local
model without treating that model as a Codex-native subagent or granting it
game, shell, repository, Git, or mutation authority.

The stable boundary is a worker protocol, not a model family:

```text
Codex or another orchestrator
  -> bounded task manifest + allowlisted evidence
  -> local-review-worker protocol
  -> runtime adapter
  -> selected local model
  -> schema-validated candidate result + provenance
  -> orchestrator verification and decision
```

Qwen, Gemma, Llama, DeepSeek, GPT-OSS, or another model can sit behind the
worker when the exact model/runtime profile has proven the capability required
by the mission. A text-only model can review supplied logs but cannot accept a
visual-review mission. A runtime that consumes memory needed by the game cannot
claim concurrent playtest operation merely because inference works alone.

## Capability negotiation

Capabilities belong to the protocol; qualification belongs to an exact local
deployment. Keep these separate:

- an adapter declares the transports and modalities it can carry;
- a worker profile records the runtime, model artifact, device placement, and
  capabilities actually tested together;
- a mission declares hard required capabilities; and
- the orchestrator rejects the mission unless the qualified profile satisfies
  every requirement.

Useful capability identifiers include `input.text`, `input.image`,
`output.closed_json`, `review.visual`, `review.text`,
`game_actions.propose_bounded`, and `runtime.concurrent_with_game`. The last
capability must be measured on the target machine. Model-family marketing or a
server's `/models` response is discovery evidence, not qualification.

The reference executable exposes `capabilities`, but its initial response is
the adapter's maximum interface—not proof that the currently selected model is
vision-capable. Conformance probes and an accepted worker profile are required
before a task can move beyond unqualified experimentation.

## Protocol v1

The reference executable supports:

```bash
python3 scripts/local-review-openai.py capabilities
python3 scripts/local-review-openai.py run \
  --request examples/local-review-task.json \
  --evidence-root /path/to/ignored/evidence \
  --endpoint http://127.0.0.1:8080/v1/chat/completions \
  --model local-vision-model
```

`run` accepts one `contracts/local-review-task.schema.json` mission and prints
one `contracts/local-review-result.schema.json` provenance envelope. The
candidate inside that envelope remains model-produced evidence, not an
approved result.

The reference adapter targets an OpenAI-compatible local image-chat endpoint.
That transport is an adapter choice rather than a protocol requirement. A
future Soul adapter, desktop runtime, or different local server can implement
the same executable commands and schemas while keeping provider selection
private.

## Current authority boundary

Version 1 is review-only and accepts text and/or images according to the task's
declared capabilities:

- one request and one terminal result;
- one to four explicit PNG, JPEG, or WebP files;
- numeric loopback HTTP only, with an exact endpoint path and explicit port;
- relative image paths resolved beneath one caller-supplied evidence root;
- request, image, aggregate-image, response, timeout, and output-count bounds;
- closed task and candidate shapes;
- evidence SHA-256 digests and model/adapter provenance;
- no API key, remote URL, arbitrary file path, shell, tool call, game control,
  source read, source write, Git, retry loop, or automatic repair.

Text visible inside a screenshot is untrusted evidence. It is not an
instruction to the worker. Captures and results belong in ignored run
directories and require privacy review before retention or publication.

## Qualification, not blanket trust

Trust is earned for a tuple, not a model name:

```text
task schema + task type + runtime/adapter version + model artifact digest
+ inference profile + device class + game build + evidence policy
```

Use this progression independently for each task type:

1. **Unqualified:** results are exploratory; the orchestrator independently
   reviews every input and finding.
2. **Observed:** a fixed evaluation set measures misses, false positives,
   malformed claims, latency, and resource coexistence; every live result is
   still verified.
3. **Qualified with audit:** only narrow, objective checks with an accepted
   error budget may avoid full duplicate review. Retain artifacts and sample
   results periodically and after every model, prompt, runtime, driver, game,
   or schema change.
4. **Revoked:** any unexplained miss, provenance mismatch, capability drift,
   or resource interference returns that task type to unqualified status.

Subjective art direction and final visual approval remain human decisions.
Qualification for missing-material detection does not confer qualification for
terrain continuity, traversal, combat feel, or any other task.

## Agentic expansion path

Keep version 1 evidence-only while it is being qualified. Later versions may
add an orchestrated journey loop without giving the model general tools:

1. the game exposes a small, schema-bounded action catalog such as look, move,
   capture, inspect-state, and stop;
2. the worker proposes one enumerated action with a reason and expected
   observation;
3. the harness validates and executes the action, then returns fresh semantic
   state and rendered evidence;
4. a strict step/time/distance budget terminates the journey; and
5. the worker emits the same provenance-bearing result envelope.

The harness—not the model—owns process launch, action execution, timeouts,
cleanup, artifact paths, and approval gates. Code changes remain outside this
worker boundary.

## Reference runtime notes

The reference adapter relies only on Python's standard library. It is designed
for local servers that support image content and schema-constrained JSON on an
OpenAI-compatible chat-completions route. Verify those features against the
exact runtime version before qualification. Runtime startup, model download,
device assignment, and model switching are intentionally out of scope.
