import time
from functions import *


def run(**kwargs):

    num_media = kwargs.get('num_media', {})
    sms_sid = kwargs.get('sms_sid', {})
    sms_from = kwargs.get('sms_from', {})
    body = kwargs.get('body', {})
    media_url = kwargs.get('media_url', {})

    # return flask forms as dict
    # data = request.form

    #  sms or mms - zero indicates sms
    flag = str(num_media)

    #  gcs bucket name - images saved here
    bucket_name = "twillio-images"

    # required to initialize vertex client
    project = "cf-data-analytics"
    loc = "us-central1"

    # process multimedia messages (mms)
    if flag != "0":

        # download image sms_from twillio
        mms_process(media_url, sms_sid)

        #  set filename of images sent to gcs. Use unique identifier sms_from twillio
        filename = sms_sid + ".png"

        # Upload image to gcs bucket
        upload_blob(bucket_name, filename, filename)

        # save metadata to firestore collection 1 (filename, masked identifier)
        save_results_collection1(
            sms_sid, number_mask(sms_from), filename)

        # create results doc
        save_results_collection2(sms_sid, filename)

    # process text messages
    else:

        #  retrieve last image URL uploaded by same user sms_from Firestore
        time.sleep(45)
        doc = return_image(number_mask(sms_from))
        filename = doc["fileName"]

        # construct gsl using filename
        path = "gs://" + bucket_name + "/" + filename  # uri

        # genrate response using gemini
        genai_ouput = generate_text(
            project, loc, path, body)

        print(genai_ouput)

        update_collection2(doc["fileName"].split(
            ".")[0], body, genai_ouput)

    return
