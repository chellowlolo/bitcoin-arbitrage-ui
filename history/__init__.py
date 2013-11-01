import app, json, logging, threading
from .models import TradeChain, Trade, ExecutedTradeChain
from websocket import WebSocket


def record_opportunity_websocket(msg):
    trade_dict = json.loads(msg)
    chain = TradeChain(**kwargs)    
    app.db.add(chain)
    
    old_trade = None

    for i in range(0, len(trade_dict.trades)):
        trade = Trade(**trade_dict.trades[i])
        trade.tradechain = chain
        trade.from_trade = old_trade
        old_trade = trade
        app.db.add(trade)

    app.db.commit()


def record_traderbot_websocket(msg):
    obj_dict = json.loads(msg)

    if "tradechain" not in obj_dict:
        return
    
    chain = ExecutedTradeChain(
        pivot_currency = obj_dict["pivot_currency"],
        profit = obj_dict["profit"],
        percentage = obj_dict["percentage"],
        starting_market = obj_dict["trades"][0]["market_name"],
        ending_market = obj_dict["trades"][-1]["market_name"]
    )

    app.db.add(chain)
    app.db.commit()


def listen_to_opportunities_websocket():
    ws = WebSocket("http://localhost:8888/")
    listen_for_opportunities = True

    while listen_for_opportunities:
        try:
            msg = ws.recv()
            record_opportunity_websocket(msg)
        except OSError:
            logging.error("[History] Could not init / websocket.")
            listen_for_opportunities = False


def listen_to_traderbot_websocket():
    ws = WebSocket("http://localhost:8888/traderbot")
    listen_for_traderbot = True

    while listen_for_traderbot:
        try:
            msg = ws.recv()
            record_traderbot_websocket(msg)
        except OSError:
            logging.error("[History] Could not init /traderbot websocket.")
            listen_for_traderbot = False


def start_recording_websockets():
    trader_thread = threading.Thread(target = listen_to_traderbot_websocket)
    trader_thread.daemon = True
    trader_thread.start()

    opp_thread = threading.Thread(target = listen_to_opportunities_websocket)
    opp_thread.daemon = True
    opp_thread.start()
