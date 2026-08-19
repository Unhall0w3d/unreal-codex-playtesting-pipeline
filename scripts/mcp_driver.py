#!/usr/bin/env python3
"""Minimal stdlib MCP Streamable HTTP driver for a game semantic provider.

This is intentionally small and synchronous. It demonstrates protocol framing,
session handling, sequential calls, and numeric smoke assertions. Adapt tool
names and result parsing to the schemas implemented by your game.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


PROTOCOL_VERSION = "2025-06-18"


def decode_response(raw: bytes, content_type: str) -> dict[str, Any]:
    text = raw.decode("utf-8")
    if "text/event-stream" not in content_type:
        return json.loads(text)

    events: list[dict[str, Any]] = []
    for line in text.splitlines():
        if line.startswith("data:"):
            events.append(json.loads(line.removeprefix("data:").strip()))
    if not events:
        raise RuntimeError("MCP server returned an empty SSE response")
    return events[-1]


@dataclass
class McpClient:
    url: str
    timeout: float = 15.0
    session_id: str | None = None
    request_id: int = 0

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.request_id += 1
        payload: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
        }
        if params is not None:
            payload["params"] = params
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "MCP-Protocol-Version": PROTOCOL_VERSION,
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            session = response.headers.get("Mcp-Session-Id")
            if session:
                self.session_id = session
            body = decode_response(response.read(), response.headers.get_content_type())
        if "error" in body:
            raise RuntimeError(f"MCP error: {body['error']}")
        return body.get("result", {})

    def initialize(self) -> dict[str, Any]:
        result = self.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "unreal-runtime-smoke", "version": "0.1.0"},
            },
        )
        self.notify("notifications/initialized")
        return result

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "MCP-Protocol-Version": PROTOCOL_VERSION,
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout):
            pass

    def call(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        result = self.request("tools/call", {"name": name, "arguments": arguments or {}})
        if result.get("isError"):
            raise RuntimeError(f"Tool {name} returned an error: {result}")
        return result

    def close(self) -> None:
        if not self.session_id:
            return
        request = urllib.request.Request(
            self.url,
            headers={
                "Mcp-Session-Id": self.session_id,
                "MCP-Protocol-Version": PROTOCOL_VERSION,
            },
            method="DELETE",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout):
                pass
        except urllib.error.HTTPError as error:
            if error.code not in (404, 405):
                raise


def structured_payload(tool_result: dict[str, Any]) -> dict[str, Any]:
    if isinstance(tool_result.get("structuredContent"), dict):
        return tool_result["structuredContent"]
    for item in tool_result.get("content", []):
        if item.get("type") == "text":
            value = json.loads(item.get("text", "{}"))
            if isinstance(value, dict):
                return value
    raise RuntimeError("Tool result did not contain structured JSON")


def smoke(client: McpClient) -> dict[str, Any]:
    before = structured_payload(client.call("game-state"))
    client.call("game-move", {"forward": 1.0, "right": 0.0, "sprint": False, "seconds": 1.0})
    time.sleep(1.2)
    after_move = structured_payload(client.call("game-state"))

    start = before["player"]["location_cm"]
    end = after_move["player"]["location_cm"]
    planar_delta = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
    if planar_delta < 25.0:
        raise AssertionError(f"Expected at least 25 cm movement, observed {planar_delta:.2f}")

    client.call("game-action", {"action": "jump"})
    time.sleep(0.1)
    after_jump = structured_payload(client.call("game-state"))
    vertical_velocity = after_jump["player"]["velocity_cm_s"][2]
    if vertical_velocity <= 0.0:
        raise AssertionError(f"Expected positive jump velocity, observed {vertical_velocity:.2f}")

    return {
        "ok": True,
        "planar_delta_cm": round(planar_delta, 2),
        "jump_velocity_cm_s": round(vertical_velocity, 2),
        "health": after_jump["player"].get("health"),
        "objective": after_jump.get("objective"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("command", choices=("smoke", "list-tools"))
    args = parser.parse_args()

    client = McpClient(args.url)
    try:
        initialized = client.initialize()
        if args.command == "list-tools":
            output = {"initialize": initialized, "tools": client.request("tools/list")}
        else:
            output = smoke(client)
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())
