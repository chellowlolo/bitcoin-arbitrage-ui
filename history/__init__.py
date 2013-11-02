import json, logging, threading
from app import db
from .models import Log, TradeChain, Trade
from websocket import create_connection, WebSocketConnectionClosedException


def record_traderbot_websocket(msg):
    msg_dict = json.loads(msg)

    if "tradechain" not in msg_dict:
        return

    chain_dict = msg_dict["tradechain"]
    chain = TradeChain(
        pivot_currency = chain_dict["pivot_currency"],
        profit = chain_dict["profit"],
        percentage = chain_dict["percentage"]
    ) 
    db.session.add(chain)
    
    old_trade = None

    for i in range(0, len(chain_dict["trades"])):
        trade = Trade(**chain_dict["trades"][i])
        trade.tradechain = chain
        trade.from_trade = old_trade
        old_trade = trade
        db.session.add(trade)

    db.session.commit()


def record_log_websocket(msg):
    db.session.add(Log(message = msg))
    db.session.commit()


def listen_to_websocket(path, record_func):
    try:
        ws = create_connection("ws://localhost:8888/%s" % path)
    except ConnectionRefusedError:
        logging.error("[History] Could not init '/%s' websocket." % path)
        return

    while True:
        try:
            msg = ws.recv()
            record_func(msg)
        except WebSocketConnectionClosedException:
            logging.error("[History] Lost connection to websocket '/%s'" % path)
            return


def start_recording_websockets():
    trader_thread = threading.Thread(
        target = listen_to_websocket,
        args = ("traderbot", record_traderbot_websocket)
    )
    trader_thread.daemon = True
    trader_thread.start()

    log_thread = threading.Thread(
        target = listen_to_websocket,
        args = ("log", record_log_websocket)
    )
    log_thread.daemon = True
    log_thread.start()
