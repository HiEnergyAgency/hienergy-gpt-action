---
name: hi-energy-api
description: Call the Hi Energy API from OpenClaw using a reusable Python request script with support for Bearer auth, custom headers, query params, and JSON payloads. Use when a user asks to fetch Hi Energy data, submit jobs/actions to Hi Energy endpoints, test Hi Energy connectivity, or troubleshoot API responses.
---

# Hi Energy API

Use this skill to make repeatable, debuggable requests to Hi Energy endpoints.

## Quick workflow

1. Set credentials from environment variables or pass them directly:
   - `HI_ENERGY_BASE_URL`
   - `HI_ENERGY_API_KEY`
2. Call `scripts/call_hi_energy.py` with `--path` and optional method/body/headers.
3. Review JSON output (`ok`, `status`, `data` or `raw`) and report the result.

## Command patterns

Health check:

```bash
python3 scripts/call_hi_energy.py --path /status
```

POST JSON body:

```bash
python3 scripts/call_hi_energy.py \
  --method POST \
  --path /jobs \
  --body '{"text":"hello"}'
```

With query parameters:

```bash
python3 scripts/call_hi_energy.py \
  --path /events \
  --query limit=20 \
  --query cursor=abc123
```

Custom auth/header override:

```bash
python3 scripts/call_hi_energy.py \
  --path /status \
  --header "x-api-key: $HI_ENERGY_API_KEY"
```

## Files

- `scripts/call_hi_energy.py` — generic API caller for Hi Energy endpoints.
- `references/api-setup.md` — setup notes and auth override example.
