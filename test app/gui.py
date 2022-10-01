import flet
from flet import Page, Row, Text, TextField, ElevatedButton, Checkbox, Column, ListView
import pprint
from server import Server, db, auth

def main(page: Page):
    serv = Server("firetest-6713b-firebase-adminsdk.json", "AIzaSyA5XEqYHw5lMt5nYwtfuB_MuDgAFLq_bYU")
    
    email = TextField(label="Email", autofocus=True)
    id = TextField(label="ID")
    password = TextField(label="Password", password=True)
    Message = TextField(label="Message")
    lv = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    page.add(lv)
    
    def call(e):
        lv.controls.clear()
        pg = auth.list_users()
        while pg:
            for user in pg.users:
                lv.controls.append(Text(serv.get(f"users/personal/{user.uid}")["message"]))
            pg = pg.get_next_page()
        page.update()
    
    db.reference("/users/personal", app=serv.app).listen(call)
    
    def btn_click(e):                
        result = serv.create_user(email.value, id.value, password.value)
        if not result:
            pass

        email.value = ""
        id.value = ""
        password.value = ""
        page.update()
        email.focus()
        
    def delete(e):
        serv.delete_user(id.value)
        id.value = ""
        
    def signin(e):
        serv.sign_in_email_and_password(email.value, password.value)
        email.value = ""
        id.value = ""
        password.value = ""
        
    def push(e):
        data = {
            "message" : Message.value
        }
        serv.push(f"users/personal/{serv.uid}/", data)
        Message.value = ""
        
    page.add(
        email,
        id,
        password,
        Row([
            ElevatedButton("SignUp", on_click=btn_click),
            ElevatedButton("SignIn", on_click=signin),
            ElevatedButton("Delete User", on_click=delete)
        ]),
        Row([
            Message,
            ElevatedButton("Push", on_click=push)
        ])
    )
    
flet.app(target=main, view=flet.WEB_BROWSER)