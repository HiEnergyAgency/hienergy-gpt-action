# Hi Energy API setup notes

Configure credentials before making requests:

```bash
export HI_ENERGY_BASE_URL="https://api.hienergy.example/v1"
export HI_ENERGY_API_KEY="<your-api-key>"
```

If Hi Energy uses a different auth header, call the script with explicit headers:

```bash
python3 scripts/call_hi_energy.py \
  --path /status \
  --header "x-api-key: $HI_ENERGY_API_KEY"
```

The script prints structured JSON with status, response headers, and parsed payload when possible.
