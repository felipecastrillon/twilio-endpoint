
from hashlib import sha256
from dotenv import load_dotenv
import requests
import os
from google.cloud import storage
import time
import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


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

    media_url = dict["MediaUrl0"]
    filename = dict["SmsSid"] + ".png"

    with open(filename, 'wb') as f:
        image_url = media_url
        f.write(requests.get(image_url).content)
    print("processing mms")


def sms_process(dict):
    print("processing sms")


def save_results(id, user, file):

    import datetime

    # ct stores current time
    ct = datetime.datetime.now()

    if not firebase_admin._apps:
        firebase_admin.initialize_app()

    db = firestore.client()

    doc_ref = db.collection("gemini-demo-text").document(id)
    doc_ref.set({"user": user, "fileName": file,
                "fileLocation": "https://storage.cloud.google.com/twillio-images/" + file,
                 "timeStamp": ct})


def return_image(user):

    if not firebase_admin._apps:
        firebase_admin.initialize_app()

    db = firestore.client()

    docs = (
        db.collection("gemini-demo-text")
        .where(filter=FieldFilter("user", "==", user))
        .order_by("timeStamp").limit_to_last(1)
        .get()
    )

    for doc in docs:
        print(doc.to_dict())
