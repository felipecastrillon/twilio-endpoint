import functions_framework
import json
from functions import *


@functions_framework.http
def main(request):

    try:
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

        ########### CORS headers compete ###########

        # return flask forms as dict
        data = request.form

        #  sms or mms - zero indicates sms
        flag = str(data["NumMedia"])

        #  gcs bucket name - images saved here
        bucket_name = "twillio-images"

        # print("flag type " + flag)

        # process multimedia messages (mms)
        if flag != "0":

            # download image from twillio
            mms_process(data)

            #  filename of images in gcs
            filename = data["SmsSid"] + ".png"

            # filename = data["SmsSid"] + ".png"

            # bucket_name = "twillio-images"
            source_file_name = filename
            destination_blob_name = filename

            # Upload image to gcs bucket
            upload_blob(bucket_name, source_file_name, destination_blob_name)

            # save metadata to firestore
            save_results(data["SmsSid"], number_mask(data["From"]), filename)

        # process text messages
        else:

            #  retrieve last image URL uploaded by same user from Firestore
            doc = return_image(number_mask(data["From"]))

            # last image URL
            # print(doc["fileName"])

            filename = doc["fileName"]

            project = "cf-data-analytics"  # required to initialize vertex client
            loc = "us-central1"
            path = "gs://" + bucket_name + "/" + filename  # uri

            genai_ouput = generate_text(
                project, loc, path, "summarize this picture in one word")

            print(genai_ouput)

        #  debug: print entire payload from twillio
        myJSON = json.dumps(data)
        print(myJSON)

    except Exception as e:
        print(e)
    return ("done", 200, headers)
