import json, logging, threading
from app import db
from .models import TradeChain, Trade, ExecutedTradeChain
from websocket import create_connection, WebSocketConnectionClosedException


def record_opportunity_websocket(msg):
    chain_dict = json.loads(msg)
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

    db.session.add(chain)
    db.session.commit()


def listen_to_opportunities_websocket():
    try:
        ws = create_connection("ws://localhost:8888/")
    except ConnectionRefusedError:
        logging.error("[History] Could not init '/' websocket.")
        return

    while True:
        try:
            msg = ws.recv()
            record_opportunity_websocket(msg)
        except WebSocketConnectionClosedException:
            logging.error("[History] Lost connection to websocket '/'")
            return


def listen_to_traderbot_websocket():
    try:
        ws = create_connection("ws://localhost:8888/traderbot")
    except ConnectionRefusedError:
        logging.error("[History] Could not init '/traderbot' websocket.")
        return

    while True:
        try:
            msg = ws.recv()
            record_traderbot_websocket(msg)
        except WebSocketConnectionClosedException:
            logging.error("[History] Lost connection to websocket '/traderbot'")
            return


def start_recording_websockets():
    trader_thread = threading.Thread(target = listen_to_traderbot_websocket)
    trader_thread.daemon = True
    trader_thread.start()

    opp_thread = threading.Thread(target = listen_to_opportunities_websocket)
    opp_thread.daemon = True
    opp_thread.start()
