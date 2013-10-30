import json
from flask import Flask, flash, redirect, request, render_template

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
path_to_config = "../bitcoin-arbitrage/arbitrage/config.json"

@app.route("/")
def show_config():

    with open(path_to_config, "r") as f:
        config = json.loads(f.read())

    return render_template("index.html", config = config)


@app.route("/update", methods=["POST"])
def update_config():
    with open(path_to_config, "r") as f:
        config = json.loads(f.read())

    with open(path_to_config, "w+") as f:
        config.update(request.form.to_dict())
        f.write(json.dumps(config))

    flash("Updated bot settings.")

    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True) 
