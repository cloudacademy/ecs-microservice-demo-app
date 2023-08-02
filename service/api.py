from bottle import Bottle, HTTPResponse
import os
import random
import string
import uuid
import mysql.connector

VERSION = "0.0.1"
BOTTLEIP = "0.0.0.0"
BOTTLEPORT = os.environ.get("SERVICE_PORT", 8080)

SERVICE = os.environ.get("SERVICE", "generic_service")

APP = Bottle(__name__)

DB_HOST = os.environ.get("DB_HOST")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
cnx = None
try:
    cnx = mysql.connector.connect(host=DB_HOST, user='root', password=DB_PASSWORD, port=3306)
    print("db connected successfully")
except Exception as e:
    print("db connection failed")
print(cnx)

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
