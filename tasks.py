from db import db
from flask import session

#Creates a new task ->
#Fetches the id of the task we created ->
#Creates a default comment for the task
def new_task(creator_id, task, priority):
    if len(task) > 50:return False
    if len(task) == 0:return False
    try:
        sql = "INSERT INTO tasks (creator_id, task, priority, made_at, done) " \
        "VALUES (:creator_id, :task, :priority, NOW(), FALSE)"
        db.session.execute(sql, {"creator_id":creator_id, "task":task, "priority":priority})
        db.session.commit()

        hae_id_sql = "SELECT id FROM tasks WHERE creator_id = :creator_id ORDER BY made_at DESC"
        task_id_from_sql = (db.session.execute(hae_id_sql, {"creator_id":creator_id}).fetchone())
        new_comment(creator_id, task_id_from_sql[0], "Click to set a comment")
    except:
        return False
    return True

#Sets the 'visible' status on the pres_with_comment(user_id):
    sql = "SELECT T.task, T.priority, T.made_at, T.id, C.comment FROM tasks AS T, " \
          vious comment as FALSE
#and then creates a new comment
def new_comment(creator_id, task_id, comment):
    if len(comment) > 500:return False
    try:
        hide_old_sql = "UPDATE comments SET visible = FALSE WHERE task_id = :task_id"
        db.session.execute(hide_old_sql, {"task_id":task_id})
        db.session.commit()
        sql = "INSERT INTO comments (creator_id, task_id, comment, visible) " \
            "VALUES (:creator_id, :task_id, :comment, TRUE)"
        db.session.execute(sql, {"creator_id":creator_id, "task_id":task_id, "comment":comment})
        db.session.commit()
    except:
        return False
    return True

def get_comment(task_id):
    sql = "SELECT comment FROM comments WHERE task_id = :task_id AND visible = TRUE"
    return db.session.execute(sql, {"task_id":task_id}).fetchone()

def get_all_tasks():
    sql = "SELECT id, task, creator_id FROM tasks ORDER BY priority"
    return db.session.execute(sql).fetchall()

def get_my_tasks_with_comment(user_id):
    sql = "SELECT T.task, T.priority, T.made_at, T.id, C.comment FROM tasks AS T, " \
        "comments AS C WHERE T.creator_id = :user_id AND T.done = FALSE AND C.task_id = T.id " \
        "AND C.visible = TRUE ORDER BY T.priority"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_my_completed_tasks(user_id):
    sql = "SELECT T.task, T.priority, T.made_at, T.id, C.comment FROM tasks AS T, " \
        "comments AS C WHERE T.creator_id = :user_id AND T.done = TRUE AND C.task_id = T.id " \
        "AND C.visible = TRUE ORDER BY T.priority"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()
def get_my_tasks(user_id):
    sql = "SELECT task, priority, made_at, id FROM tasks WHERE creator_id = :user_id " \
        "AND done = FALSE ORDER BY priority"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()
    
def get_task_info(id):
    sql = "SELECT * FROM tasks WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def task_done(task_id, user_id):
    sql = "UPDATE tasks SET done=TRUE WHERE id=:id AND creator_id = :user_id"
    db.session.execute(sql, {"id":task_id, "user_id":user_id})
    db.session.commit()