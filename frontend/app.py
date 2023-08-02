from bottle import Bottle, jinja2_template, TEMPLATE_PATH, static_file, HTTPResponse
import os
import requests

VERSION = "0.0.1"
BOTTLEIP = "0.0.0.0"
BOTTLEPORT = os.environ.get("SERVICE_PORT", 8080)

SERVICE_HOST = os.environ.get("SERVICE_HOST", "")
SERVICES = [s for s in os.environ.get("SERVICES", "").split(",") if s]


APP = Bottle(__name__)
TEMPLATE_PATH.insert(0, "/root")


def get_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("response", [])


@APP.route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="static")


@APP.route("/")
def index():
    tables = []
    message = ""

    for service in SERVICES:
        if not service or service == "":
            continue
        url = f"http://{SERVICE_HOST}/{service}"
        try:
            data = get_data(url)
            tables.append(data)
        except Exception as e:
            message = str(e)

    return jinja2_template("index.html", tables=tables, message=message)


@APP.route("/ok", method=["GET"])
def ok():
    response = HTTPResponse(status=200, body="OK!\n")
    response.content_type = "text/plain"
    return response


if __name__ == "__main__":
    try:
        SERVER = APP.run(host=BOTTLEIP, port=BOTTLEPORT, debug=True)
    except KeyboardInterrupt:
        pass
        print("exiting...")
        SERVER.stop()
