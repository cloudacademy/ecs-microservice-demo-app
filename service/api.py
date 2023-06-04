from bottle import Bottle, HTTPResponse
import os
import random
import string
import uuid

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.bottle.middleware import XRayMiddleware
from aws_xray_sdk.core import patch_all

xray_recorder.configure(service='frontend')
plugins = ('EC2Plugin', 'EC2Plugin')
xray_recorder.configure(plugins=plugins)
patch_all()

VERSION = "0.0.1"
BOTTLEIP = "0.0.0.0"
BOTTLEPORT = os.environ.get("SERVICE_PORT", 8080)

SERVICE = os.environ.get("SERVICE", "generic_service")


APP = Bottle(__name__)

xray_recorder.configure(service=SERVICE, dynamic_naming=SERVICE)
APP.install(XRayMiddleware(xray_recorder))

def generate_records():
    records = []

    for i in range(10):
        record_id = str(uuid.uuid4())
        name = "".join(random.choices(string.ascii_uppercase, k=5))
        field1 = "".join(random.choices(string.ascii_lowercase, k=5))
        field2 = "".join(random.choices(string.ascii_lowercase, k=5))
        field3 = "".join(random.choices(string.ascii_lowercase, k=5))

        name = f"{SERVICE}_{name}"
        field1 = f"{SERVICE}_{field1}"
        field2 = f"{field2}_{SERVICE}"
        field3 = f"{field3}_{SERVICE}"

        records.append(
            {
                "id": record_id,
                "name": name,
                "field1": field1,
                "field2": field2,
                "field3": field3,
            }
        )

    return records


@APP.route(f"/{SERVICE}", method=["OPTIONS", "GET"])
def data():
    try:
        body = generate_records()

        response = HTTPResponse(status=200, body={"response": body})
        response.content_type = "application/json"
        return response
    except Exception as err:
        print(err)
        body = {"version": VERSION, "message": err}
        response = HTTPResponse(status=400, body={"response": body})
        return response


if __name__ == "__main__":
    try:
        SERVER = APP.run(host=BOTTLEIP, port=BOTTLEPORT, debug=True)
    except KeyboardInterrupt:
        pass
        print("exiting...")
        SERVER.stop()
