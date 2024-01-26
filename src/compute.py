import time
from functions import *


def run(**kwargs):

    delay = 25

    try:
        # num_media = kwargs.get('num_media', {})
        sms_sid = kwargs.get('sms_sid', {})
        sms_from = kwargs.get('sms_from', {})
        body = kwargs.get('body', {})
        media_url = kwargs.get('media_url', {})
        dtype = kwargs.get('dtype', {})

        #  gcs bucket name - images saved here
        bucket_name = "twillio-images"

        # required to initialize vertex client
        project = "cf-data-analytics"
        loc = "us-central1"

        # process multimedia messages (mms)
        if dtype == "mms":

            # download image sms_from twillio
            mms_process(media_url, sms_sid)

            #  set filename of images sent to gcs. Use unique identifier sms_from twillio
            filename = sms_sid + ".png"

            print("processing file: " + filename)

            # Upload image to gcs bucket
            upload_blob(bucket_name, filename, filename)

            print("upload to bucket complete")

            # save metadata to firestore collection 1 (filename, masked identifier)
            save_results_collection1(
                sms_sid, number_mask(sms_from), filename)

            print("Meta data saved to Firestore")

            # create results doc
            save_results_collection2(sms_sid, filename)

            print("Filename saved to collection 2")

        elif dtype == "both":

            print("processing both")

            # download image sms_from twillio
            mms_process(media_url, sms_sid)

            #  set filename of images sent to gcs. Use unique identifier sms_from twillio
            filename = sms_sid + ".png"

            print("processing file: " + filename)

            # Upload image to gcs bucket
            upload_blob(bucket_name, filename, filename)

            print("upload to bucket complete")

            # save metadata to firestore collection 1 (filename, masked identifier)
            save_results_collection1(
                sms_sid, number_mask(sms_from), filename)

            print("Meta data saved to Firestore")

            # create results doc
            save_results_collection2(sms_sid, filename)

            print("Filename saved to collection 2")

            ################################## processes text #################################

            print("processing sms")

            for i in range(delay):
                time.sleep(1)
                print(i)

            doc = return_image(number_mask(sms_from))

            print("doc returned from Firestore")
            print(doc)

            filename = doc["fileName"]

            # construct gsl using filename
            path = "gs://" + bucket_name + "/" + filename  # uri

            print("file path: " + path)
            print("body: " + body)
            print("project: " + project)

            print(type(body))

            # genrate response using gemini
            genai_ouput = generate_text(
                project, loc, path, body)

            print(genai_ouput)

            update_collection2(doc["fileName"].split(
                ".")[0], body, genai_ouput)

        # process text messages
        elif body == "sms":
            #  retrieve last image URL uploaded by same user sms_from Firestore

            print("processing sms")

            for i in range(delay):
                time.sleep(1)
                print(i)

            doc = return_image(number_mask(sms_from))

            print("doc returned from Firestore")
            print(doc)

            filename = doc["fileName"]

            # construct gsl using filename
            path = "gs://" + bucket_name + "/" + filename  # uri

            # genrate response using gemini
            genai_ouput = generate_text(
                project, loc, path, body)

            print(genai_ouput)

            # upload results to firestore
            update_collection2(doc["fileName"].split(
                ".")[0], body, genai_ouput)

    except Exception as e:
        print(e)
