
from hashlib import sha256
from dotenv import load_dotenv
import os


def number_mask(hash_str):

    load_dotenv()

    key = os.getenv('HMAC_VAL')

    val = hash_str + key

    print(sha256(val.encode('utf-8')).hexdigest())

    out = sha256(val.encode('utf-8')).hexdigest()

    return out
