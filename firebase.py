# import pyrebase

# config = {
#     "apiKey": "AIzaSyBfgOuF_dUT7vFjb1BIt6ffG7K0vsiAQHg",
#     "authDomain": "silicon-comfort-260315.appspot.com",
#     "databaseURL": "https://silicon-comfort-260315.appspot.com",
#     "projectId": "silicon-comfort-260315",
#     "storageBucket": "silicon-comfort-260315.appspot.com",
#     "messagingSenderId": "5947928423"
# }

# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()

# img_name = 'image/1580876123.jpg'

# storage.child( img_name ).download('image.jpg')

import pyrebase

def firebase_init():
    config = {
        "apiKey": "AIzaSyBfgOuF_dUT7vFjb1BIt6ffG7K0vsiAQHg",
        "authDomain": "silicon-comfort-260315.appspot.com",
        "databaseURL": "https://silicon-comfort-260315.appspot.com",
        "projectId": "silicon-comfort-260315",
        "storageBucket": "silicon-comfort-260315.appspot.com",
        "messagingSenderId": "5947928423"
    }
    
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    return storage

# storage.child('image/new.jpg').put('image.jpg')
# storage.child('image/new.jpg').download('example.jpg')
# print(storage.child("image/new.jpg").get_url(None))