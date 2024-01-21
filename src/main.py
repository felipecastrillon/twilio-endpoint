import functions_framework
import json
from functions import *


@functions_framework.http
def main(request):

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

    data = request.get_data()

    res = json.loads(data.value.decode('unicode_escape'))

    print(request.get_data())

    print("request recieved")

    print(res)

    return ("done", 200, headers)
