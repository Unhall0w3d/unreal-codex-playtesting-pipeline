#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
adapter="${repo_root}/scripts/capture-hyprland-window.sh.example"
test_root="$(mktemp -d)"
trap 'rm -rf -- "$test_root"' EXIT

mock_bin="${test_root}/bin"
mkdir -p -- "$mock_bin"
touch "${test_root}/Game.uproject"

cat >"${mock_bin}/fake-editor" <<'EOF'
#!/usr/bin/env bash
touch "$MOCK_LAUNCHED"
printf '%s\n' READY_FOR_CAPTURE
sleep 30
EOF

cat >"${mock_bin}/hyprctl" <<'EOF'
#!/usr/bin/env bash
case "${1:-}" in
  workspaces)
    printf '%s\n' '[{"id":7,"monitor":"HDMI-A-1"}]'
    ;;
  clients)
    if [[ -e "$MOCK_LAUNCHED" ]]; then
      printf '%s\n' '[{"address":"0xold","mapped":true,"class":"Terminal","title":"Terminal","at":[0,0],"size":[800,600],"workspace":{"name":"1"}},{"address":"0xgame","mapped":true,"class":"UnrealEditor","title":"Game","at":[1920,0],"size":[1600,900],"workspace":{"name":"7"}}]'
    else
      printf '%s\n' '[{"address":"0xold","mapped":true,"class":"Terminal","title":"Terminal","at":[0,0],"size":[800,600],"workspace":{"name":"1"}}]'
    fi
    ;;
  activewindow)
    if [[ "${MOCK_FOCUS_MODE:-preserve}" == "steal" && -e "$MOCK_LAUNCHED" ]]; then
      printf '%s\n' '{"address":"0xgame"}'
    else
      printf '%s\n' '{"address":"0xold"}'
    fi
    ;;
  cursorpos)
    printf '%s\n' '{"x":320,"y":240}'
    ;;
  eval|dispatch)
    printf '%s\n' "$*" >>"$MOCK_CALLS"
    printf '%s\n' ok
    ;;
  *)
    printf 'unexpected hyprctl invocation: %s\n' "$*" >&2
    exit 1
    ;;
esac
EOF

cat >"${mock_bin}/grim" <<'EOF'
#!/usr/bin/env bash
output="${!#}"
printf '%s' PNG >"$output"
EOF

chmod +x "${mock_bin}/fake-editor" "${mock_bin}/hyprctl" "${mock_bin}/grim"

run_adapter() {
  local case_name=$1
  local focus_mode=$2
  local output="${test_root}/${case_name}/capture.png"
  mkdir -p -- "$(dirname -- "$output")"
  rm -f -- "${test_root}/launched" "${test_root}/calls"
  PATH="${mock_bin}:$PATH" \
    MOCK_LAUNCHED="${test_root}/launched" \
    MOCK_CALLS="${test_root}/calls" \
    MOCK_FOCUS_MODE="$focus_mode" \
    bash "$adapter" \
      --editor "${mock_bin}/fake-editor" \
      --project "${test_root}/Game.uproject" \
      --output "$output" \
      --workspace 7 \
      --ready-marker READY_FOR_CAPTURE \
      --timeout-seconds 5 \
      --capture-timeout-seconds 2 \
      --window-regex 'UnrealEditor Game' \
      --initial-class-regex '^(UnrealEditor)$'
}

run_adapter success preserve
[[ -s "${test_root}/success/capture.png" ]]
grep -Fq 'no_focus = true' "${test_root}/calls"
grep -Fq 'r:set_enabled(false)' "${test_root}/calls"

if run_adapter focus-theft steal >"${test_root}/focus-theft.out" 2>"${test_root}/focus-theft.err"; then
  echo "focus-theft case unexpectedly succeeded" >&2
  exit 1
fi
[[ ! -e "${test_root}/focus-theft/capture.png" ]]
grep -Eq '(newly-created|captured) client took focus' "${test_root}/focus-theft.err"
grep -Fq 'dispatch focuswindow address:0xold' "${test_root}/calls"
grep -Fq 'dispatch movecursor 320 240' "${test_root}/calls"
grep -Fq 'r:set_enabled(false)' "${test_root}/calls"

echo "Hyprland capture adapter tests passed"
