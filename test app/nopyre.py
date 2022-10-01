import json
import requests
import pprint

from typing import Optional

import firebase_admin
from firebase_admin import auth

# initialize server
from firebase_admin import credentials
cred = credentials.Certificate("firetest-6713b-firebase-adminsdk.json")
app = firebase_admin.initialize_app(cred)


API_KEY = "AIzaSyA5XEqYHw5lMt5nYwtfuB_MuDgAFLq_bYU"
api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

def create_user(email: str, user_id: Optional[str], password: Optional[str]):
    return auth.create_user(email=email, uid=user_id, password=password) if user_id else auth.create_user(email=email)

def update_email(user_id: str, email: str):
    return auth.update_user(user_id, email=email)


def update_mobile(user_id: str, mobile_no: str):
    return auth.update_user(user_id, phone_number=mobile_no)


def update_display_name(user_id: str, display_name: str):
    return auth.update_user(user_id, display_name=display_name)

def sign_in_with_email_and_password(email, password, token: bool = True):
    payload = json.dumps({
        "email" : email,
        "password" : password,
        "returnSecureToken" : token
    })
    
    r = requests.post(api_url,
                      params={"key" : API_KEY},
                      data=payload)
    
    return r.json()

def delete_user(id):
    return auth.delete_user(id)

if __name__ == "__main__":
    email = "yuksungmin975@gmail.com"
    id = "sungmin"
    pw = "1234567"
    
    #new_user = create_user(email, id, pw)
    token = sign_in_with_email_and_password(email, pw)
    pprint.pprint(token)
    # update_user = update_email("sungmin", email)
    # update_user = update_mobile("sungmin", "+12345678")
    # update_user = update_display_name("sungmin", "육성민")