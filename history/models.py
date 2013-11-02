from app import db


class DictAttrs(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Log(DictAttrs, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    message = db.Column(db.Text)


class TradeChain(DictAttrs, db.Model):
    __tablename__ = "tradechain"

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    pivot_currency = db.Column(db.String(3))
    profit = db.Column(db.Float)
    percentage = db.Column(db.Float)
    trades = db.relationship("Trade", backref="tradechain")


class Trade(DictAttrs, db.Model):
    __tablename__ = "trade"

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    price = db.Column(db.Float)
    amount = db.Column(db.Float)
    price_currency = db.Column(db.String(3))
    amount_currency = db.Column(db.String(3))
    type = db.Column(db.String(4))
    market_name = db.Column(db.String(20))
    from_trade = db.relationship(
        "Trade", uselist=False, backref="to_trade", remote_side=[id]
    )
    from_trade_id = db.Column(db.Integer, db.ForeignKey("trade.id"))
    tradechain_id = db.Column(db.Integer, db.ForeignKey("tradechain.id"))

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
