import app

class DictAttrs(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TradeChain(DictAttrs, app.db.Model):
    __tablename__ = "tradechain"

    id = app.db.Column(app.db.Integer, primary_key = True)
    created_at = app.db.Column(app.db.DateTime, default = app.db.func.now())
    pivot_currency = app.db.Column(app.db.String(3))
    profit = app.db.Column(app.db.Float)
    percentage = app.db.Column(app.db.Float)
    trades = app.db.relationship("Trade", backref="tradechain")


class Trade(DictAttrs, app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key = True)
    created_at = app.db.Column(app.db.DateTime, default = app.db.func.now())
    price = app.db.Column(app.db.Float)
    amount = app.db.Column(app.db.Float)
    price_currency = app.db.Column(app.db.String(3))
    amount_currency = app.db.Column(app.db.String(3))
    type = app.db.Column(app.db.String(4))
    market_name = app.db.Column(app.db.String(20))
    from_trade = app.db.relationship(
        "Trade", uselist=False, backref="to_trade", remote_side=[id]
    )
    from_trade_id = app.db.Column(app.db.Integer, app.db.ForeignKey("trade.id"))
    tradechain_id = app.db.Column(app.db.Integer, app.db.ForeignKey("tradechain.id"))

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

class ExecutedTradeChain(DictAttrs, app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key = True)
    created_at = app.db.Column(app.db.DateTime, default = app.db.func.now())
    pivot_currency = app.db.Column(app.db.String(3))
    starting_market = app.db.Column(app.db.String(20))
    ending_market = app.db.Column(app.db.String(20))
    profit = app.db.Column(app.db.Float)
    percentage = app.db.Column(app.db.Float)
 
