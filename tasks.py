from db import db
from flask import session

def new_task(creator_id, task, priority):
    print(creator_id, task, priority)
    try:
        sql = "INSERT INTO tasks (creator_id, task, priority, made_at, done) VALUES (:creator_id, :task, :priority, NOW(), FALSE)"
        db.session.execute(sql, {"creator_id":creator_id, "task":task, "priority":priority})
        db.session.commit()
        print("uuden taskin luonti onnistui")
    except:
        print("virhe sql:ssä taskia luodessa")
        return False
    return True
    