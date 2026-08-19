# Contributing

Contributions are welcome when they keep the package generic, safe to publish,
and useful as a reference implementation. By contributing, you agree that your
contribution may be distributed under the repository's Apache License 2.0.

Minimum expectations:

1. Preserve the non-Shipping and loopback security boundaries.
2. Add no credentials, personal paths, proprietary assets, or engine files.
3. Attribute incorporated third-party work and identify modifications.
4. Run shell syntax checks, Python compilation/tests, secret scanning, and the
   relevant Unreal build/package matrix.
5. Include exact commands and evidence in change descriptions.
6. Keep machine-qualified behavior separate from human-approved feel/visuals.

Please explain the security boundary affected by a change, include the
commands you ran, and avoid adding real project assets or credentials. Changes
that broaden runtime automation beyond the stated loopback, non-Shipping
boundary need a separate threat-model discussion before implementation.
