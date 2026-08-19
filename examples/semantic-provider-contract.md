# Semantic provider contract

Implement this contract inside a non-Shipping Unreal runtime plugin or game
module. Names are examples; prefer a stable project prefix if tools may coexist.

## `game-state`

Return structured, authoritative values such as:

```json
{
  "player": {
    "location_cm": [0.0, 0.0, 100.0],
    "velocity_cm_s": [0.0, 0.0, 0.0],
    "health": 100.0,
    "defeated": false
  },
  "camera": {"yaw_deg": 0.0, "pitch_deg": -10.0},
  "objective": {"id": "smoke.start", "complete": false},
  "enemies": [],
  "frame": 1,
  "world_seconds": 0.0
}
```

## `game-move`

Inputs: `forward` and `right` in `[-1, 1]`, `sprint` boolean, and `seconds`
in `[0.05, 5]`. Drive mapped input, never set actor transform directly. Cancel
the previous release timer before a new movement command and release all keys
on completion, cancellation, world teardown, and provider shutdown.

## `game-action`

Accept only a fixed enum such as `jump`, `dodge`, `light-attack`,
`heavy-attack`, `lock-toggle`, `ability-1` through `ability-8`, and `stop`.
Reject unknown strings. `stop` releases held input and cancels active timers.

## `game-look`

Clamp yaw to `[-180, 180]` degrees and pitch to `[-90, 90]` per call. Use the
game's camera input path.

## Destructive test tools

Damage and reset tools must be separately named, schema-bounded, disabled in
Shipping, and approval-gated by the client. Return before/after state and a
clear result. Do not expose a general cheat or console command.

## Capture

Write PNGs beneath one fixed ignored automation directory. Generate filenames
inside the game; do not accept paths from callers. Enforce a 12 MiB limit both
before and after reading the file. Return image content with `image/png`.

## Threading and lifecycle

Execute Unreal operations serially on the game thread. Use weak references for
world objects, unregister tools on shutdown, cancel timers on world teardown,
and never allow the provider to create a network listener in Shipping.
