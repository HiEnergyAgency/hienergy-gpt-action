---
name: hi-energy-ai-api
description: Call the Hi Energy AI API for chat/completions-style requests, health checks, and generic REST operations from the terminal. Use when a user asks to send prompts to Hi Energy AI, test API auth, debug request/response errors, or automate repeated API calls with consistent headers and payload patterns.
---

# Hi Energy AI API

Use this skill to make reliable Hi Energy AI API calls with minimal guesswork.

## Quick start

1. Export credentials and base URL:

```bash
export HI_ENERGY_API_KEY="<token>"
export HI_ENERGY_BASE_URL="https://api.hienergy.ai"
```

2. Run the helper script:

```bash
./scripts/call_hi_energy_api.sh \
  --path /v1/chat/completions \
  --payload-file references/example-chat-payload.json
```

## Workflow

1. Validate required env vars:
   - `HI_ENERGY_API_KEY`
   - `HI_ENERGY_BASE_URL`
2. Start with a health/info endpoint (if available) to verify auth.
3. Send a minimal request body first.
4. Expand payload fields only after a successful baseline request.
5. If the API returns errors, inspect HTTP status + response body and retry with corrected params.

## Common commands

### Chat-style POST request

```bash
./scripts/call_hi_energy_api.sh \
  --path /v1/chat/completions \
  --payload-file references/example-chat-payload.json
```

### Generic GET request

```bash
./scripts/call_hi_energy_api.sh --method GET --path /v1/models
```

### Add extra header

```bash
./scripts/call_hi_energy_api.sh \
  --path /v1/chat/completions \
  --payload-file references/example-chat-payload.json \
  --header "X-Client: openclaw"
```

## Debug checklist

- `401/403`: verify API key, token prefix, org/project scope, and env var export.
- `404`: confirm `HI_ENERGY_BASE_URL` and endpoint path.
- `422/400`: validate JSON schema and required fields.
- `429`: backoff and retry.
- `5xx`: retry with jitter and capture response body for incident notes.

## Resources

- `scripts/call_hi_energy_api.sh` — generic authenticated API caller.
- `references/example-chat-payload.json` — starter payload template for chat/completions style APIs.