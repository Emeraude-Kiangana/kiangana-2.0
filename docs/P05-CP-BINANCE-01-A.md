# P05-CP-BINANCE-01-A — RDC Connectivity & Adapter Foundation

Status: OPEN / RDC connectivity pending. Issue: #10.

Python stdlib-only read-only Binance public market data. Only `/api/v3/ticker/price` and `/api/v3/exchangeInfo` at `https://data-api.binance.vision`; fixed symbol allowlist; no credentials, orders, withdrawals, leverage or authenticated endpoints. CI is offline and mocked; it **does not prove connectivity from DRC**.

Run physically from a DRC network:

```bash
python3 -m unittest discover -s tests -p 'test_binance_public.py' -v
python3 -m scripts.rdc_probe
```

Review `rdc-connectivity-evidence.json` before sharing. Manually attest location only when true. Do not publish IP, credentials or personal details. A network or geographic restriction is a failed gate, not an instruction to circumvent it. Binance connector in ChatGPT is distinct from this standalone REST adapter and from any official standalone MCP server. KIF V0.2 remains on historical branch; no KIF merge claimed.
