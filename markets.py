from collections import OrderedDict

ALL_MARKETS = {
    "Btce": [
        ["BTC", "USD"],
        ["BTC", "RUR"],
        ["BTC", "EUR"],
        ["LTC", "BTC"],
        ["LTC", "USD"],
        ["LTC", "RUR"],
        ["LTC", "EUR"],
        ["NMC", "BTC"],
        ["NMC", "USD"],
        ["NVC", "BTC"],
        ["NVC", "USD"],
        ["USD", "RUR"],
        ["EUR", "USD"],
        ["TRC", "BTC"],
        ["PPC", "BTC"],
        ["FTC", "BTC"],
        ["XPM", "BTC"]
    ],
    "Bitstamp": [
        ["BTC", "USD"]
    ],
    "BitcoinCentral": [
        ["BTC", "EUR"]
    ],
    "MtGox": [
        ["BTC", "USD"]
    ]
}
ALL_MARKETS = OrderedDict(sorted(ALL_MARKETS.items(), key=lambda t: t[0]))
