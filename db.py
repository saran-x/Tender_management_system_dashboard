from dotenv import load_dotenv,find_dotenv
from pymongo import MongoClient
import os
import pprint
printer=pprint.PrettyPrinter()
load_dotenv(find_dotenv())
load_dotenv(find_dotenv())
password=os.environ.get('mongo_db_password')
connection_db=f"mongodb+srv://saranrajtsaranrajt27:{password}""@saran.kz45sjy.mongodb.net/?retryWrites=true&w=majority&appName=saran"
client=MongoClient(connection_db)
db_tender=client.tendor
v_tender=db_tender.tendor_place
v_tenders=db_tender.vendor
counts=v_tenders.find_one({'status':'Awarded'})

printer.pprint(counts)

client.close()