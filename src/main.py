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

    data = request.form

    # if data["numMedia"] != "0":
    #     print("start")

    mms_process(data)

    print("mms done")

    filename = data["SmsSid"] + ".png"

    # destination_file = os.path.realpath(os.path.join(
    #     os.path.dirname(__file__), '..')) + "/images/" + filename

    bucket_name = "twillio-images"
    source_file_name = "/images/" + filename

    destination_blob_name = filename

    upload_blob(bucket_name, source_file_name, destination_blob_name)

    print("upload to gcs complete")
    # else:
    #     sms_process(data)

    # Converting to JSON format
    myJSON = json.dumps(data)

    print(number_mask(data["From"]))

    # Displaying the JSON format
    print(myJSON)

    return ("done", 200, headers)
