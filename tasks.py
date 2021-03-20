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

def new_comment(creator_id, task_id, comment):
    print(creator_id, task_id, comment)
    sql = "INSERT INTO comments (creator_id, task_id, comment) VALUES (:creator_id, :task_id, :comment)"
    db.session.execute(sql, {"creator_id":creator_id, "task_id":task_id, "comment":comment})
    db.session.commit()

def get_comment(task_id):
    print("tultiin get comment metodiin, task_id ->")
    sql = "SELECT comment FROM comments WHERE task_id = :task_id"
    return db.session.execute(sql, {"task_id":task_id}).fetchone()

def get_all_tasks():
    sql = "SELECT id, task, creator_id FROM tasks ORDER BY priority"
    return db.session.execute(sql).fetchall()

def get_my_tasks_with_comment(user_id):
    sql = "SELECT T.task, T.priority, T.made_at, T.id, C.comment FROM tasks AS T, comments AS C WHERE T.creator_id = 1 AND T.done = FALSE AND C.task_id = T.id ORDER BY T.priority"


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