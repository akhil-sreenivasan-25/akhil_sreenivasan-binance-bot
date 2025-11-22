import hmac, hashlib, time

api_secret = 's6b0mo3gO3IIZKdGjo0pGgbPYTTS84EJRxq7hO0Ah81btVP7MyuiiiqwaziTUN3q'

params = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "quantity": 0.01,
    "price": 35000,
    "timeInForce": "GTC",
    "timestamp": int(time.time() * 1000)
}

query_string = "&".join([f"{k}={v}" for k,v in params.items()])
signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
params["signature"] = signature