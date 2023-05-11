import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import os

DIR_PATH = os.path.abspath(os.getcwd())


def initializeFirebaseDB():
    cred = credentials.Certificate(DIR_PATH+"/service_account_key.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()