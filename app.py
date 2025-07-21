
# app.py
from markupsafe import Markup
from flask import Flask, render_template, request
from bot import SpotTradingBot, API_KEY, API_SECRET

app = Flask(__name__)
bot = SpotTradingBot(API_KEY, API_SECRET, testnet=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        symbol = request.form["symbol"].upper()
        side = request.form["side"].upper()
        order_type = request.form["order_type"].upper()
        quantity = float(request.form["quantity"])
        price = float(request.form["price"]) if order_type == "LIMIT" else None

        result = bot.place_order(symbol, side, order_type, quantity, price)

        if isinstance(result, dict) and "error" in result:
            message = f"❌ Error: {result['error']}"
        else:
            message = f"""
✅ Order placed successfully!<br>
<b>Symbol:</b> {result['symbol']}<br>
<b>Order ID:</b> {result['orderId']}<br>
<b>Status:</b> {result['status']}<br>
<b>Side:</b> {result['side']}<br>
<b>Type:</b> {result['type']}<br>
<b>Quantity:</b> {result['origQty']}<br>
<b>Executed Qty:</b> {result['executedQty']}<br>
<b>Price:</b> {result['fills'][0]['price'] if 'fills' in result and result['fills'] else 'N/A'}<br>
"""

    return render_template("index.html", message=Markup(message))

if __name__ == "__main__":
    app.run(debug=True)
