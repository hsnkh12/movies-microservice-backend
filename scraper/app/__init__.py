from celery import Celery
import os
from dotenv import load_dotenv
from .db_config import initializeFirebaseDB
from .database import DB
load_dotenv()


app = Celery('scraper', broker='amqps://jqdjczml:wVihh1Yey_UtdpuEdxC-Bjef2kcxhzRu@hummingbird.rmq.cloudamqp.com/jqdjczml',task_serializer='json')
conn = initializeFirebaseDB()

print(f"Database connection: {conn}")

db = DB(conn)

