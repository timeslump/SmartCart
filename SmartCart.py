import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/smartcart-94000-firebase-adminsdk-pkypl-72ca0b7711.json')
default_app = firebase_admin.initialize_app(cred, {'databaseURL':'https://smartcart-94000-default-rtdb.firebaseio.com/'})
itemprice = db.reference('Item').get()
for x in itemprice:
    print(itemprice[x]['price'])
nitemprice = { x:itemprice[x]['price'] for x in itemprice}

    
print(nitemprice)