# Security policy

## Supported versions

This starter package is not a released runtime and has no supported version.
Security fixes will be made against the default branch until a release policy
is established.

## Reporting a vulnerability

Use this repository's GitHub Private Vulnerability Reporting channel. Do not
publish exploitable details in a public issue. If that channel is unavailable,
open a minimal public issue requesting a private contact path and omit all
reproduction details.

Please include the affected version, platform, reproduction steps, impact, and
whether the issue can expose the automation listener beyond loopback.

## Security boundary

Runtime automation must be absent from Shipping, explicitly enabled in test
builds, loopback-only unless authenticated for a reviewed remote threat model,
and restricted to narrow schema-validated tools.
