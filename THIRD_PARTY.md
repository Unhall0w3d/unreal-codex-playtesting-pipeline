# Third-party attribution and boundaries

This starter bundle contains original documentation and templates only. It does
not redistribute the software or assets listed below.

## Unreal Engine

Unreal Engine is developed by Epic Games, Inc. It is not bundled here. Users
must obtain it from Epic and comply with the applicable Unreal Engine license.

- https://www.unrealengine.com/
- https://www.unrealengine.com/eula/unreal

Do not commit Unreal Engine files or Epic Marketplace/Fab content to a public
repository unless the applicable terms expressly permit that distribution.

## Unreal-MCP

- Project: https://github.com/IvanMurzak/Unreal-MCP
- Author/copyright: Ivan Murzak
- License reported by upstream: Apache License 2.0
- Tested historical pin: `v0.13.1`, commit
  `86fc73d7da25b069845139bb9d378aabfc92a2e6`

If source from this project is incorporated, retain the upstream license and
notices and clearly identify modifications.

## GameDev-MCP-Server

- Project: https://github.com/IvanMurzak/GameDev-MCP-Server
- Author/copyright: Ivan Murzak
- License reported by upstream: Apache License 2.0
- Tested historical pin: `v9.2.4`

If source or binaries from this project are redistributed, retain the upstream
license and notices and satisfy the Apache-2.0 terms.

## Model Context Protocol

- Specification: https://modelcontextprotocol.io/specification/

MCP is an interoperability protocol. Refer to the specification project for
its current terms and attribution requirements.

## OpenAI Codex

- Documentation: https://developers.openai.com/codex/

Codex is not bundled. Users obtain and configure it separately under OpenAI's
applicable terms.

## Desktop capture prerequisites

The optional `scripts/capture-hyprland-window.sh.example` invokes software
already installed by the user; it does not redistribute or vendor these tools:

- [Hyprland](https://hyprland.org/) and its [`hyprctl` Lua/eval interface](https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/)
- [`jq`](https://jqlang.org/)
- [`grim`](https://gitlab.freedesktop.org/emersion/grim)

Check each project's current license, package provenance, and compatibility
before installing. The example contains no source or binaries from them.

## Optional local-model runtimes

The local-review worker does not bundle a model or inference runtime. It may be
connected to software obtained separately by the user, including:

- [llama.cpp](https://github.com/ggml-org/llama.cpp), whose upstream repository
  reports the MIT License; and
- [Qwen](https://github.com/QwenLM), whose individual model and code artifacts
  must be checked for their exact license before download or redistribution.

The protocol does not require either project. Record the model artifact,
runtime version, applicable license, and provenance in each deployment.

## Repository license

The original material in this repository is licensed under Apache License 2.0,
as recorded in [LICENSE-DECISION.md](LICENSE-DECISION.md). That selection does
not change or supersede any third-party license.
