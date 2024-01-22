
from hashlib import sha256
from dotenv import load_dotenv
import requests
import os
from google.cloud import storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    generation_match_precondition = 0

    blob.upload_from_filename(
        source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def number_mask(hash_str):

    load_dotenv()

    # load salt secret
    key = os.getenv('HMAC_VAL')

    # concatenate hash and salt
    val = hash_str + key

    # print(sha256(val.encode('utf-8')).hexdigest())

    # hash the concatenated string
    out = sha256(val.encode('utf-8')).hexdigest()

    return out


def mms_process(dict):

    # media_url = "https://api.twilio.com/2010-04-01/Accounts/AC26d1f8d778dbb994a245d009031c15df/Messages/MM5d61e6c40b3d39bd2af2134570123a89/Media/ME7c6a0ed52668d7c9b4d5cbef9ba71d24"
    # filename = "MM5d61e6c40b3d39bd2af2134570123a89.png"

    media_url = dict["MediaUrl0"]
    filename = dict["SmsSid"] + ".png"

    # DOWNLOAD_DIRECTORY = os.path.realpath(os.path.join(
    #     os.path.dirname(__file__), '..')) + "/src"

    DOWNLOAD_DIRECTORY = ""

    # r = requests.get(media_url, stream=True)

    with open(filename, 'wb') as f:
        image_url = media_url
        f.write(requests.get(image_url).content)
    print("processing mms")


def sms_process(dict):
    print("processing sms")
