from app import db


class DictAttrs(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TradeChain(db.Model, DictAttrs):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    pivot_currency = db.Column(db.String(3))
    profit = db.Column(db.Float)
    percentage = db.Column(db.Float)



class Trade(db.Model, DictAttrs):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    price = db.Column(db.Float)
    amount = db.Column(db.Float)
    price_currency = db.Column(db.String(3))
    amount_currency = db.Column(db.String(3))
    type = db.Column(db.String(4))
    market_name = db.Column(db.String(20))
    from_trade = db.relationship("Trade", backref="to_trade")
    tradechain = db.relationship("TradeChain", backref="trades", lazy="dynamic")

    @property
    def to_volume(self):
        return self.amount if self.type == "buy" \
        else self.price

    @property
    def to_currency(self):
        return self.amount_currency if self.type == "buy" \
        else self.price_currency
         
    @property
    def from_volume(self):
        return self.amount if self.type == "sell" \
        else self.price
         
    @property
    def from_currency(self):
        return self.amount_currency if self.type == "sell" \
        else self.price_currency

class ExecutedTradeChain(db.Model, DictAttrs):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    pivot_currency = db.Column(db.String(3))
    starting_market = db.Column(db.String(20))
    ending_market = db.Column(db.String(20))
    profit = db.Column(db.Float)
    percentage = db.Column(db.Float)
 
