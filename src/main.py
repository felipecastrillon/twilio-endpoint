import threading
import functions_framework
# import json
from functions import *
from compute import *
# import time


@functions_framework.http
def main(request):

    data = request.form

    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    # num_media = str(data["NumMedia"])

    if "MediaUrl0" in data and "Body" in data:
        print("sms and mms")
        dtype = "both"
        url = data["MediaUrl0"]
        body = data["Body"]
    elif "MediaUrl0" in "Body" not in data:
        print("mms")
        dtype = "mms"
        url = data["MediaUrl0"]
        body = ""
    elif "Body" in data and "MediaUrl0" not in data:
        print("sms")
        dtype = "sms"
        url = ""
        body = data["Body"]

    print("starting threaded app")

    print(data)

    thread = threading.Thread(target=run, kwargs={
        'dtype': dtype,
        'body': body,
        'num_media': data["NumMedia"],
        'sms_sid': data["SmsSid"],
        'sms_from': data["From"],
        'media_url': url})
    thread.start()

    return ("done", 200, headers)
