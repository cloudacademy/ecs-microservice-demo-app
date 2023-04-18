from bottle import Bottle, jinja2_template, TEMPLATE_PATH
import os
import requests

VERSION = "0.0.1"
BOTTLEIP = "0.0.0.0"
BOTTLEPORT = os.environ.get("SERVICE_PORT", 8080)

SERVICE_HOST = os.environ.get("INTERNAL_ALB", "")
SERVICES = os.environ.get("SERVICES", "").split(",")


APP = Bottle(__name__)
TEMPLATE_PATH.insert(0, "/root")


@APP.route("/")
def index():
    tables = []

    for service in SERVICES:
        if not service:
            continue
        url = f"{SERVICE_HOST}/{service}"
        response = requests.get(url).json()
        tables.append(response["response"])

    return jinja2_template("index.html", tables=tables)


if __name__ == "__main__":
    try:
        SERVER = APP.run(host=BOTTLEIP, port=BOTTLEPORT, debug=True)
    except KeyboardInterrupt:
        pass
        print("exiting...")
        SERVER.stop()
