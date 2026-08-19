# Security and privacy checklist

## Before committing

- [ ] No personal home paths, usernames, hostnames, account IDs, machine IDs,
      browser profiles, task/thread IDs, or private repository URLs.
- [ ] No tokens, cookies, passwords, API keys, OAuth material, or credential
      stores.
- [ ] No Unreal Engine, Marketplace/Fab, or other non-redistributable assets.
- [ ] Every incorporated dependency has a license and attribution record.
- [ ] Download URLs use HTTPS and every archive and installed executable is
      verified with a reviewed checksum or stronger provenance mechanism.
- [ ] Generated logs and captures are ignored; sample evidence is manually
      reviewed for private UI, paths, player names, and notifications.

## Runtime boundary

- [ ] Automation code and dependencies are excluded from Shipping.
- [ ] Listener creation, connection, and child processes require an explicit
      non-Shipping automation flag.
- [ ] Unauthenticated services are forced to loopback; environment variables
      cannot widen the bind address.
- [ ] Hostnames and resolved addresses are validated as loopback.
- [ ] Tools are narrowly scoped, schema-validated, bounded, and serialized on
      the game thread.
- [ ] Shell, console, arbitrary reflection, arbitrary file access, asset
      mutation, and actor spawning are unavailable to runtime tests.
- [ ] Destructive tools retain approval and emit auditable results.
- [ ] Screenshot output is fixed, traversal-safe, and size-limited both before
      and after reading.

## Harness lifecycle

- [ ] A fresh server PID and listener identity are verified.
- [ ] A whole-harness timeout encloses setup, server, game, driver, and cleanup.
- [ ] Per-command timeouts also exist.
- [ ] EXIT, INT, and TERM cleanup kills and waits for every owned child.
- [ ] Cleanup proves no child or listener survived.
- [ ] Each run has a unique evidence directory and a machine-readable result.

## Before release

- [ ] Editor Development, game Development, and game Shipping targets compile.
- [ ] Shipping has no runtime automation dependency.
- [ ] Cook/stage/PAK/archive succeeds from a clean checkout.
- [ ] Headless state tests and rendered capture tests both pass.
- [ ] Secret scanning, shell syntax, Python tests, and checksum verification run
      in CI.
- [ ] A clean-room installation succeeds without private files or cached state.
- [ ] An independent security review has been completed.
- [ ] Human review has approved controls, feel, visuals, accessibility, and
      evidence retention.
