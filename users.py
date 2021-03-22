from db import db
from flask import session, request, abort
import os
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    print(password)
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print(user)
    if user == None:
        return False
    else:
        print("mentiin elseen")
        print(user[0])
        print(password)
        print("nyt pitäs mennä läpi?")
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["username"] = username
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def check_user(creator_id, user_id):
    if creator_id != user_id:
        print("eri idt")
        abort(403)

def check_csrf():
    print("csrf check")
    if session["csrf_token"] != request.form["csrf_token"]:
        print("abort")
        abort(403)