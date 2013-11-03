import json

path_to_config = "../bitcoin-arbitrage/arbitrage/config.json"

def update(new_config):
    with open(path_to_config, "r") as f:
        try:
            config = json.loads(f.read())
        except ValueError:
            config = {}

    with open(path_to_config, "w+") as f:
        for key, value in new_config.items():
            try:
                new_config[key] = int(value)
            except (ValueError, TypeError):
                try:
                    new_config[key] = float(value)
                except (ValueError, TypeError):
                    new_config[key] = value

        config.update(new_config)
        f.write(json.dumps(config))

def get():
    try:
        with open(path_to_config, "r") as f:
            config = json.loads(f.read())
        return config
    except FileNotFoundError:
        return {}
