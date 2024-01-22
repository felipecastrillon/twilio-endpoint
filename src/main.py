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

    flag = str(data["MediaContentType0"])

    print("flag type" + flag)

    if flag == "image/png":
        print("mms")
    else:
        print("not mms")

    # download image from twillio
    mms_process(data)

    # list directory
    for x in os.listdir():
        print(x)

    filename = data["SmsSid"] + ".png"

    bucket_name = "twillio-images"
    source_file_name = filename
    destination_blob_name = filename

    # Upload image to gcs bucket
    upload_blob(bucket_name, source_file_name, destination_blob_name)

    # save metadata to firestore
    save_results(data["SmsSid"], number_mask(data["From"]), filename)

    # else:
    #     sms_process(data)

    # Converting to JSON format
    myJSON = json.dumps(data)

    # print(number_mask(data["From"]))

    # Displaying the JSON format
    print(myJSON)

    return ("done", 200, headers)
