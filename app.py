import config, markets
from flask import Flask, flash, redirect, request, \
    render_template, make_response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/btc-arb-ui.db"
db = SQLAlchemy(app)

# The history module depends on the db variable defined above.
import history


@app.route("/feed", methods=["GET"])
def show_feed():
    return render_template("feed.html", port = 8888) 

@app.route("/settings", methods=["GET"])
def show_settings():
    return render_template("settings.html", config = config.get())

@app.route("/settings", methods=["POST"])
def update_settings():
    config.update(request.form.to_dict())
    flash("Updated bot settings.")

    return redirect("/settings")

@app.route("/markets", methods=["GET"])
def show_markets():
    return render_template("markets.html",
        markets = config.get().get("markets", {}), all_markets = markets.ALL_MARKETS
    )
 
@app.route("/markets", methods=["POST"])
def update_markets():
    markets = {}
    for market_currency_pair in request.form.getlist("markets"):
        market, currency1, currency2 = tuple(market_currency_pair.split("_"))
        if market not in markets:
            markets[market] = []
        markets[market].append((currency1, currency2))

    config.update({"markets": markets})
    flash("Updated markets being watched.")

    return redirect("/markets")

@app.route("/history", methods=["GET"])
def history_form():
    return render_template("history.html", config = config.get())

@app.route("/history", methods=["POST"])
def history_download():
    csv = ""

    if request.form["type"] == "chains":
        orders = history.models.ExecutedTradeChain.query.all()
        csv = "Timestamp,Currency,Profit,Profit (%),"\
            + "Starting Market,Ending Market\r\n"
    
        for order in orders:
            csv += "%s,%s,%s,%s,%s,%s\r\n" % (
                order.created_at, order.pivot_currency,
                order.profit, order.percentage,
                order.starting_market, order.ending_market
            )
    elif request.form["type"] == "trades":
        trades = history.models.ExecutedTrade.query.all()

    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=%s.csv" % (
        request.form["type"]
    )
    return response


if __name__ == "__main__":
    history.start_recording_websockets()
    app.run(debug=True) 
