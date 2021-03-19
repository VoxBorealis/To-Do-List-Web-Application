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

def get_all_tasks():
    sql = "SELECT id, task, creator_id FROM tasks ORDER BY priority"
    return db.session.execute(sql).fetchall()

def get_my_tasks(user_id):
    sql = "SELECT task, priority, made_at, id FROM tasks WHERE creator_id = :user_id AND done = FALSE ORDER BY priority"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()
    
def get_task_info(id):
    sql = "SELECT * FROM tasks WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def task_done(task_id, user_id):
    sql = "UPDATE tasks SET done=TRUE WHERE id=:id AND creator_id = :user_id"
    db.session.execute(sql, {"id":task_id, "user_id":user_id})
    db.session.commit()
    print("done onnistui sql")