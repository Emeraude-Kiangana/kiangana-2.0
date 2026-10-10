import io
import json
import unittest
from urllib.error import HTTPError, URLError
from src.binance_public import BinancePublicDataAdapter, BinancePublicDataError

class Response:
    status = 200
    def __init__(self, payload): self.payload = io.BytesIO(json.dumps(payload).encode())
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, n): return self.payload.read(n)

class Tests(unittest.TestCase):
    def test_price(self):
        a = BinancePublicDataAdapter(opener=lambda req, timeout: Response({"symbol": "BTCUSDT", "price": "123.45"}))
        self.assertEqual(a.get_spot_price("BTCUSDT")["data"]["price"], "123.45")
    def test_exchange_info(self):
        a = BinancePublicDataAdapter(opener=lambda req, timeout: Response({"symbols": [{"symbol": "BTCUSDT", "status": "TRADING"}]}))
        self.assertEqual(a.get_exchange_info("BTCUSDT")["data"]["symbols"][0]["status"], "TRADING")
    def test_allowlist(self):
        a = BinancePublicDataAdapter(opener=lambda req, timeout: self.fail("unexpected network"))
        with self.assertRaises(ValueError): a.get_spot_price("DOGEUSDT")
    def test_negative_price(self):
        a = BinancePublicDataAdapter(opener=lambda req, timeout: Response({"symbol": "BTCUSDT", "price": "-1"}))
        with self.assertRaises(BinancePublicDataError): a.get_spot_price("BTCUSDT")
    def test_wrong_symbol(self):
        a = BinancePublicDataAdapter(opener=lambda req, timeout: Response({"symbol": "ETHUSDT", "price": "1"}))
        with self.assertRaises(BinancePublicDataError): a.get_spot_price("BTCUSDT")
    def test_no_retry_429(self):
        calls = []
        error = HTTPError("https://example.invalid", 429, "rate limit", {}, io.BytesIO(b""))
        def opener(req, timeout):
            calls.append(1)
            raise error
        a = BinancePublicDataAdapter(opener=opener, retries=2)
        try:
            with self.assertRaises(BinancePublicDataError):
                a.get_spot_price("BTCUSDT")
            self.assertEqual(len(calls), 1)
        finally:
            error.close()
    def test_no_trade_methods(self):
        self.assertFalse(hasattr(BinancePublicDataAdapter(), "place_order"))

if __name__ == "__main__": unittest.main()
