
from hashlib import sha256
from dotenv import load_dotenv


def number_mask(hash_str):

    load_dotenv()

    key = os.getenv('hmac_val')

    val = hash_str + key

    print(sha256(val.encode('utf-8')).hexdigest())
