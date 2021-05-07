from db import db
from flask import session, request, abort
import os
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
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

def get_user_id_from_username(username):
    try:
        sql = "SELECT id FROM users WHERE username = :username"
        return_id = db.session.execute(sql, {"username":username}).fetchone()
    except:
        return False
    if return_id != None:
        return return_id[0]


def get_username_from_id(id):
    try:
        sql = "SELECT username FROM users WHERE id = :id"
        username = db.session.execute(sql, {"id":id}).fetchone()
    except:
        return False
    if username != None:
        return username[0]

def check_user(creator_id, user_id):
    if creator_id != user_id:
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)