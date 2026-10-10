# P05-CP-BINANCE-01-A — RDC connectivity evidence (2026-10-10)

## Scope and provenance

Evidence category: **user-provided local terminal output and user attestation**, not independent remote geolocation or remote execution by ChatGPT. User explicitly attested: physically in the Democratic Republic of the Congo, normal Internet connection, **no VPN and no proxy** during the tests. Do not interpret this as regulatory authorization, nationwide service availability, or independent location verification.

## Local execution observations

- Environment: Ubuntu/Linux in WSL2.
- Branch: `p05-cp-binance-01a-public-adapter`; clean working tree before running the probe.
- Offline unit tests: **7/7 PASS** (one non-failing Python `ResourceWarning` in mocked HTTP 429 test).
- Initial `rdc_probe` execution at `2026-10-10T08:36:28.304501+00:00`: **both checks failed** with `network unavailable`. Cause not established.
- Subsequent terminal curl: `data-api.binance.vision` and `api.binance.com` both returned **HTTP 200** for public `BTCUSDT` ticker; HTTPS to GitHub returned HTTP 200.
- Python `urllib.request.urlopen` returned **HTTP 200** and valid ticker JSON; Python reported proxy configuration `{}` and `HTTPS_PROXY configured: False`.
- `BinancePublicDataAdapter(timeout=15).get_spot_price("BTCUSDT")`: **PASS**, timestamp `2026-10-10T09:13:27.098790+00:00`, canonical JSON SHA-256 `48cdba4648bd30d732d567e39f7d6d3afde85a56129be8281a2cd4f74a10af6b`.
- Successful `python3 -m scripts.rdc_probe`: started `2026-10-10T09:13:42.573506+00:00`; `price.success=true` and `exchange_info.success=true`.
- Price response hash: `97aed9bc3211cb316d329c32e93e002ab5eeca7ce08583b5cf6fadd5331cbabe`, observed `2026-10-10T09:13:44.003719+00:00`.
- Exchange-info response hash: `e7854700093ac34f80f8a5e878e0b673711cd11f7e77595a8da4a242a261d40f`, observed `2026-10-10T09:13:45.451833+00:00`.
- The original generated JSON contains `local_network_attested: false` because the script does not automatically establish physical location; **this is not altered or misrepresented**. The user's subsequent explicit attestation is recorded separately in this document.

## GitHub CI evidence (prior head commit)

For PR #11 head `92c7ada3eb59e71d16576a294847984061dce210`, GitHub reported completed/success:
- Binance Public Data Gate: run `37976467231`.
- Gate Zero: run `37976465971`.

**These run IDs apply to the prior commit. Any later commit requires a fresh CI check.**

## Security and limitations

- No IP addresses, credentials, API keys, cookies, wallet details, or user-specific identifying data are included in this evidence record.
- The quoted hashes are self-reported program outputs; without preserved signed response bodies, they do not independently establish Binance's provenance.
- Connectivity evidence proves successful access **on one attested network at one point in time**, not permanent access or availability across the DRC.
- Public market data only: no trading, withdrawals, account access, or authentication.
- KIF integration and standalone official Binance MCP server compatibility are separate, pending gates.
- Original local JSON should remain untracked until privacy review; this Markdown record is a sanitized evidence summary.

## Exit criteria and decision

**RDC connectivity sub-gate: PASS (user-attested, locally reproduced).**
**Adapter foundation: PASS (local tests and initial CI).**
**Overall P05-CP-BINANCE-01-A: READY FOR REVIEW**, pending CI on this evidence commit and code review. Do not mark merged or production-ready.
