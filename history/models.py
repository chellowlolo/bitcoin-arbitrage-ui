from app import db

class TradeChain(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    pivot_currency = db.Column(db.String(3))
    profit = db.Column(db.Float)
    percentage = db.Column(db.Float)
    trades = db.relationship("Trade", backref="tradechain", lazy="dynamic")

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    price = db.Column(db.Float)
    amount = db.Column(db.Float)
    price_currency = db.Column(db.String(3))
    amount_currency = db.Column(db.String(3))
    type = db.Column(db.String(4))
    market_name = db.Column(db.String(20))
    to_trade = db.relationship("Trade")

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

class ExecutedTradeChain(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Colume(db.DateTime, default = db.func.now())
    pivot_currency = db.Column(db.String(3))
    starting_market = db.Column(db.String(20))
    ending_market = db.Column(db.String(20))
    profit = db.Column(db.Float)
    percentage = db.Column(db.Float)
 
