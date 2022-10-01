from datetime import datetime as dt
import pyrebase

config = {
  "apiKey": "AIzaSyA5XEqYHw5lMt5nYwtfuB_MuDgAFLq_bYU",
  "authDomain": "firetest-6713b.firebaseapp.com",
  "databaseURL": "https://firetest-6713b-default-rtdb.firebaseio.com",
  "storageBucket": "firetest-6713b.appspot.com"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

email = "yuksungmin975@gmail.com"
password = "test1234*"

#
# try:
#     auth.create_user_with_email_and_password(email, password)
# except:
#     print("aleady exists")

# Log the user in
user = auth.sign_in_with_email_and_password(email, password)
user = auth.refresh(user['refreshToken'])
user_id = auth.get_account_info(user['idToken'])['users'][0]['localId']

#auth.send_email_verification(user['idToken'])

# Get a reference to the database service
db = firebase.database()
# data to save
data = {
    "name": "Hello World",
    "pushed time": dt.now().strftime('%Y-%m-%d %H:%M:%S')
}
# Pass the user's idToken to the push method
results = db.child("users").child(user_id).set(data, user['idToken'])

# storage
storage = firebase.storage()
results = storage.child(f"users/{user_id}/test.png").put('test.png', user['idToken'])

# download file from storage
storage.child(f"users/{user_id}/test.png").download("downloaded.png")
