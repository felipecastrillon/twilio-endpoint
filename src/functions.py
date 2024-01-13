import firebase_admin
from firebase_admin import firestore


def results():

    if not firebase_admin._apps:
        firebase_admin.initialize_app()

    db = firestore.client()

    cities_ref = db.collection("gemini-demo-images")
    query = cities_ref.order_by(
        "timeStamp", direction=firestore.Query.DESCENDING).limit(3)
    results = query.stream()

    outputArray = []
    outputDict = {}

    for doc in results:
        outputArray.append(doc.to_dict())

    outputDict["data"] = outputArray

    return outputDict
