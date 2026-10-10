"""Read-only Binance Spot public API. Standard library only."""
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://data-api.binance.vision"
PATHS = {"price": "/api/v3/ticker/price", "exchange_info": "/api/v3/exchangeInfo"}
ALLOWLIST = {"BTCUSDT", "ETHUSDT", "BNBUSDT"}

class BinancePublicDataError(Exception):
    pass

class BinancePublicDataAdapter:
    def __init__(self, timeout=8, retries=1, opener=None):
        if timeout <= 0 or retries not in (0, 1, 2):
            raise ValueError("invalid timeout/retries")
        self.timeout, self.retries, self.opener = timeout, retries, opener or urlopen

    def _fetch(self, kind, symbol):
        if symbol not in ALLOWLIST:
            raise ValueError("symbol not allowlisted")
        url = BASE + PATHS[kind] + "?" + urlencode({"symbol": symbol})
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "KIANGANA-P05-ReadOnly/0.1"}, method="GET")
        for attempt in range(self.retries + 1):
            try:
                with self.opener(request, timeout=self.timeout) as response:
                    if getattr(response, "status", 200) != 200:
                        raise BinancePublicDataError("unexpected HTTP status")
                    raw = response.read(262145)
                if len(raw) > 262144:
                    raise BinancePublicDataError("response too large")
                data = json.loads(raw)
                if not isinstance(data, dict):
                    raise BinancePublicDataError("unexpected response")
                if kind == "price":
                    if data.get("symbol") != symbol or not isinstance(data.get("price"), str):
                        raise BinancePublicDataError("ticker schema invalid")
                    try:
                        price = Decimal(data["price"])
                        if not price.is_finite() or price <= 0:
                            raise BinancePublicDataError("invalid price")
                    except InvalidOperation:
                        raise BinancePublicDataError("invalid price") from None
                elif not isinstance(data.get("symbols"), list) or not any(isinstance(x, dict) and x.get("symbol") == symbol for x in data["symbols"]):
                    raise BinancePublicDataError("exchangeInfo schema invalid")
                canonical = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
                return {"source": "Binance public Spot REST", "symbol": symbol, "observed_at_utc": datetime.now(timezone.utc).isoformat(), "sha256": hashlib.sha256(canonical).hexdigest(), "data": data}
            except HTTPError as exc:
                if exc.code in (418, 429, 451) or attempt == self.retries or exc.code < 500:
                    raise BinancePublicDataError("HTTP " + str(exc.code)) from None
            except (URLError, TimeoutError, ConnectionError):
                if attempt == self.retries:
                    raise BinancePublicDataError("network unavailable") from None
            except (OSError, ValueError, UnicodeError) as exc:
                raise BinancePublicDataError("invalid response: " + type(exc).__name__) from None

    def get_spot_price(self, symbol):
        return self._fetch("price", symbol)

    def get_exchange_info(self, symbol):
        return self._fetch("exchange_info", symbol)
