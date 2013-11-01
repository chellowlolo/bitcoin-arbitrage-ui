import app, json, logging, threading
from .models import TradeChain, Trade, ExecutedTradeChain
from websocket import create_connection


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
    try:
        ws = create_connection("ws://localhost:8888/")
    except ConnectionRefusedError:
        logging.error("[History] Could not init / websocket.")
        return

    while True:
        try:
            msg = ws.recv()
            record_opportunity_websocket(msg)
        except OSError:
            logging.error("[History] Fatal error reading socket: %s" % str(e))
            return


def listen_to_traderbot_websocket():
    try:
        ws = create_connection("ws://localhost:8888/traderbot")
    except ConnectionRefusedError:
        logging.error("[History] Could not init /traderbot websocket.")
        return

    while True:
        try:
            msg = ws.recv()
            record_traderbot_websocket(msg)
        except OSError as e:
            logging.error("[History] Fatal error reading socket: %s" % str(e))
            return


def start_recording_websockets():
    trader_thread = threading.Thread(target = listen_to_traderbot_websocket)
    trader_thread.daemon = True
    trader_thread.start()

    opp_thread = threading.Thread(target = listen_to_opportunities_websocket)
    opp_thread.daemon = True
    opp_thread.start()
