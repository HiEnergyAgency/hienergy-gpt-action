#!/usr/bin/env python3
"""Call the Hi Energy API with configurable method, path, headers, and JSON body.

Examples:
  export HI_ENERGY_BASE_URL="https://api.hienergy.example/v1"
  export HI_ENERGY_API_KEY="your-secret-key"

  python3 scripts/call_hi_energy.py --path /status
  python3 scripts/call_hi_energy.py --method POST --path /jobs --body '{"text":"hello"}'
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def parse_headers(values: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for value in values:
        if ":" not in value:
            raise ValueError(f"Invalid header '{value}'. Use 'Name: Value'.")
        name, raw = value.split(":", 1)
        headers[name.strip()] = raw.strip()
    return headers


def main() -> int:
    parser = argparse.ArgumentParser(description="Call the Hi Energy API")
    parser.add_argument("--base-url", default=os.getenv("HI_ENERGY_BASE_URL", ""), help="API base URL. Defaults to HI_ENERGY_BASE_URL")
    parser.add_argument("--api-key", default=os.getenv("HI_ENERGY_API_KEY", ""), help="API key. Defaults to HI_ENERGY_API_KEY")
    parser.add_argument("--method", default="GET", help="HTTP method (GET, POST, PUT, PATCH, DELETE)")
    parser.add_argument("--path", required=True, help="Endpoint path, e.g. /status or /jobs")
    parser.add_argument("--query", action="append", default=[], help="Query parameter in key=value form. Repeatable")
    parser.add_argument("--header", action="append", default=[], help="Extra header in 'Name: Value' form. Repeatable")
    parser.add_argument("--body", help="Inline JSON string body")
    parser.add_argument("--body-file", help="Path to JSON file body")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")

    args = parser.parse_args()

    if not args.base_url:
        print("Error: Missing base URL. Set --base-url or HI_ENERGY_BASE_URL.", file=sys.stderr)
        return 2

    base = args.base_url.rstrip("/") + "/"
    path = args.path.lstrip("/")
    url = urllib.parse.urljoin(base, path)

    if args.query:
        pairs: list[tuple[str, str]] = []
        for item in args.query:
            if "=" not in item:
                print(f"Error: Invalid --query '{item}'. Use key=value.", file=sys.stderr)
                return 2
            k, v = item.split("=", 1)
            pairs.append((k, v))
        url = f"{url}?{urllib.parse.urlencode(pairs)}"

    method = args.method.upper()
    body_bytes = None
    if args.body and args.body_file:
        print("Error: Use either --body or --body-file, not both.", file=sys.stderr)
        return 2

    if args.body:
        try:
            parsed = json.loads(args.body)
        except json.JSONDecodeError as exc:
            print(f"Error: --body is not valid JSON: {exc}", file=sys.stderr)
            return 2
        body_bytes = json.dumps(parsed).encode("utf-8")

    if args.body_file:
        try:
            with open(args.body_file, "r", encoding="utf-8") as f:
                parsed = json.load(f)
        except FileNotFoundError:
            print(f"Error: body file not found: {args.body_file}", file=sys.stderr)
            return 2
        except json.JSONDecodeError as exc:
            print(f"Error: body file is not valid JSON: {exc}", file=sys.stderr)
            return 2
        body_bytes = json.dumps(parsed).encode("utf-8")

    headers = {
        "Accept": "application/json",
    }

    if args.api_key:
        headers["Authorization"] = f"Bearer {args.api_key}"

    if body_bytes is not None:
        headers["Content-Type"] = "application/json"

    try:
        headers.update(parse_headers(args.header))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    req = urllib.request.Request(url=url, data=body_bytes, method=method, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            content_type = resp.headers.get("Content-Type", "")
            output = {
                "ok": True,
                "status": resp.status,
                "url": url,
                "method": method,
                "headers": dict(resp.headers.items()),
            }
            if "application/json" in content_type:
                try:
                    output["data"] = json.loads(raw)
                except json.JSONDecodeError:
                    output["raw"] = raw
            else:
                output["raw"] = raw
            print(json.dumps(output, indent=2, ensure_ascii=False))
            return 0
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        out = {
            "ok": False,
            "status": exc.code,
            "reason": exc.reason,
            "url": url,
            "method": method,
            "raw": raw,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 1
    except urllib.error.URLError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
