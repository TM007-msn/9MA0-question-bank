"""PreToolUse hook: block any Bash or PowerShell command that mentions the mock papers.

The mock papers (reserved series) live outside the project, in the folder set
by RESERVED_DIR in scripts/paths.py. As a backstop, any shell command whose
text contains "reserved" (any case) is refused, so no command can list, open
or copy them by accident.

Claude Code passes the tool call as JSON on stdin. Exit code 2 blocks the
call and shows stderr to Claude; exit code 0 lets it through.
"""

import json
import sys


def main():
    raw = sys.stdin.read()
    try:
        command = json.loads(raw).get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError):
        # If the payload can't be parsed, judge the raw text instead, so a
        # malformed payload can't slip a forbidden command through.
        command = raw
    if "reserved" in str(command).lower():
        print("Blocked: shell commands may not mention 'reserved'. The mock papers are off limits "
              "(see CLAUDE.md). If this is unrelated (e.g. a commit message), reword it.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
