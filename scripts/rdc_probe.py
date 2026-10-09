"""Run physically on a DRC network; never publish an IP address or secrets."""
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
from src.binance_public import BinancePublicDataAdapter, BinancePublicDataError

report = {"checkpoint": "P05-CP-BINANCE-01-A", "utc": datetime.now(timezone.utc).isoformat(), "platform": platform.system(), "local_network_attested": False, "checks": {}}
a = BinancePublicDataAdapter()
for label, fn in (("price", a.get_spot_price), ("exchange_info", a.get_exchange_info)):
    try:
        result = fn("BTCUSDT")
        report["checks"][label] = {"success": True, "sha256": result["sha256"], "observed_at_utc": result["observed_at_utc"]}
    except (BinancePublicDataError, ValueError) as exc:
        report["checks"][label] = {"success": False, "error": str(exc)}
Path("rdc-connectivity-evidence.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
print("Attest DRC location manually; review before publishing.")
