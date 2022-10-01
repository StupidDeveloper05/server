from datetime import datetime as dt
import json
import requests

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import db

class Server:
    def __init__(self, api_sdk_path, api_key):
        self.uid = ""        
        self.app = firebase_admin.App
        apps = firebase_admin._apps
        if apps != None and len(apps) != 0:
            for app in apps:
                if app == firebase_admin._DEFAULT_APP_NAME:
                    self.app = firebase_admin.get_app(app)
        else:
            cred = credentials.Certificate(api_sdk_path)
            self.app = firebase_admin.initialize_app(credential=cred, 
                                                     options={
                                                        "databaseURL" : "https://firetest-6713b-default-rtdb.firebaseio.com/"
                                                    })
            
        self.api_key = api_key
        self.signinurl = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        
    # user functions
    def create_user(self, email, id, password):
        try:
            auth.create_user(email=email, uid=id, password=password)
            self.sign_in_email_and_password(email, password)            
        except:
            return False
        
    def sign_in_email_and_password(self, email, password):
        post_data = json.dumps({
            "email" : email,
            "password" : password,
            "returnSecureToken" : True
        })
        
        r = requests.post(self.signinurl,
                          params={"key" : self.api_key},
                          data=post_data)
        
        r = r.json()
        try:
            self.uid = r['localId']
            auth.set_custom_user_claims(self.uid, {'admin' : True})
        except:
            pass        
        
        return r
    
    def delete_user(self, id):
        try:
            auth.delete_user(id)
            db.reference(f"users/personal/{id}/").delete()
        except:
            pass
    
    # database functions
    def push(self, path, data):
        database = db.reference(path)
        database.update(data)
        
    def get(self, path):
        database = db.reference(path)
        try:
            return database.get()
        except:
            pass