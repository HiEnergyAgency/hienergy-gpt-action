# HiEnergy Affiliate Copilot - Custom GPT Action

Use this GPT to find and manage affiliate programs, exclusive deals, and transaction data directly from ChatGPT.

## Setup

1. Go to [ChatGPT - My GPTs](https://chat.openai.com/gpts/editor) -> **Create a GPT**.
2. **Name**: HiEnergy Affiliate Copilot
3. **Description**: Your AI affiliate manager for finding active deals, tracking commissions, and discovering new partners.
4. **Instructions**: Paste the content of `INSTRUCTIONS.md` below.
5. **Actions**:
   - Click "Create new action".
   - Paste the content of `openapi.yaml`.
   - Under **Authentication**, select "API Key".
   - Auth Type: **API Key**.
   - API Key: `X-Api-Key` (in header).
   - Enter your HiEnergy API key.
6. **Save** and start chatting!

## Usage Examples

- "Find active, exclusive fashion deals in the US."
- "Show me which advertisers approved my application this week."
- "What were my top 5 commissions last month?"
- "Find contact info for Nike affiliate managers."

## Repository

This repository contains the OpenAPI schema and instructions needed to configure the GPT action.
