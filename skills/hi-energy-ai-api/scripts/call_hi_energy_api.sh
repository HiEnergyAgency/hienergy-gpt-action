#!/usr/bin/env bash
set -euo pipefail

METHOD="POST"
PATH_ONLY=""
PAYLOAD_FILE=""
EXTRA_HEADERS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --method)
      METHOD="$2"
      shift 2
      ;;
    --path)
      PATH_ONLY="$2"
      shift 2
      ;;
    --payload-file)
      PAYLOAD_FILE="$2"
      shift 2
      ;;
    --header)
      EXTRA_HEADERS+=("$2")
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "${HI_ENERGY_API_KEY:-}" ]]; then
  echo "HI_ENERGY_API_KEY is required" >&2
  exit 1
fi

if [[ -z "${HI_ENERGY_BASE_URL:-}" ]]; then
  echo "HI_ENERGY_BASE_URL is required (example: https://api.hienergy.ai)" >&2
  exit 1
fi

if [[ -z "$PATH_ONLY" ]]; then
  echo "--path is required (example: /v1/chat/completions)" >&2
  exit 1
fi

URL="${HI_ENERGY_BASE_URL%/}${PATH_ONLY}"

CURL_ARGS=(
  -sS
  -X "$METHOD"
  "$URL"
  -H "Authorization: Bearer $HI_ENERGY_API_KEY"
  -H "Content-Type: application/json"
)

for h in "${EXTRA_HEADERS[@]}"; do
  CURL_ARGS+=( -H "$h" )
done

if [[ -n "$PAYLOAD_FILE" ]]; then
  if [[ ! -f "$PAYLOAD_FILE" ]]; then
    echo "Payload file not found: $PAYLOAD_FILE" >&2
    exit 1
  fi
  CURL_ARGS+=( --data-binary "@$PAYLOAD_FILE" )
fi

HTTP_CODE=$(curl "${CURL_ARGS[@]}" -w "\n%{http_code}")
BODY=$(printf "%s" "$HTTP_CODE" | sed '$d')
STATUS=$(printf "%s" "$HTTP_CODE" | tail -n1)

echo "$BODY"
echo "\n---"
echo "HTTP $STATUS"

if [[ "$STATUS" -ge 400 ]]; then
  exit 1
fi
