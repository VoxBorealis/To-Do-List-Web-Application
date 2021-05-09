#I had to name this 'proj' because the functions wouldn't
#work if it was named 'projects'...
from db import db
from flask import session, abort
import users

def new_project(creator_id, project):
    if len(project) < 1: return False
    if len(project) > 50: return False
    try:
        sql = "INSERT INTO projects (creator_id, project, made_at, done) VALUES (:creator_id, :project, NOW(), FALSE)"
        db.session.execute(sql, {"creator_id":creator_id, "project":project})
        db.session.commit()

        hae_id_sql = "SELECT id FROM projects WHERE creator_id = :creator_id AND project = :project"
        project_id_from_sql = (db.session.execute(hae_id_sql, {"creator_id":creator_id, "project":project}).fetchone())
        new_project_member(project_id_from_sql[0], creator_id)
    except:
        return False
    return True

def check_if_user_already_in_project(project_id, user_id):
    sql = "SELECT U.id from users AS U, project_members AS M WHERE :user_id = M.user_id AND :project_id = M.project_id"
    result = db.session.execute(sql, {"user_id":user_id, "project_id":project_id}).fetchone()
    if result == None:
        return False
    else:
        return True

def new_project_member(project_id, user_id):
    if check_if_user_already_in_project(project_id, user_id):
        return True
    else:
        try:
            sql = "INSERT INTO project_members (project_id, user_id) VALUES (:project_id, :user_id)"
            db.session.execute(sql, {"project_id":project_id, "user_id":user_id})  
            db.session.commit()
        except:
            return False
        return True

def get_project_members(project_id):
    sql = "SELECT U.username FROM project_members AS M, users AS U WHERE M.project_id = :project_id " \
           "AND M.user_id = U.id ORDER BY M.id"
    results = db.session.execute(sql, {"project_id":project_id}).fetchall()
    return results

def new_project_task_comment(creator_id, task_id, comment):
    if len(comment) > 500:return False
    try:
        sql = "INSERT INTO project_task_comments " \
            "(project_task_id, creator_id, comment, made_at, visible)" \
            " VALUES (:project_task_id, :creator_id, :comment, NOW(), TRUE)"
        db.session.execute(sql, {"project_task_id":task_id, "creator_id":creator_id,
                         "comment":comment})
        db.session.commit()
    except:
        return False
    return True

def new_project_task(project_id, creator_id, task, priority):
    if len(task) > 50 or len(task) == 0:return False
    try:
        sql = "INSERT INTO project_tasks (project_id, creator_id, task, priority, made_at, done) " \
              "VALUES (:project_id, :creator_id, :task, :priority, NOW(), FALSE)"
        db.session.execute(sql, {"project_id":project_id, "creator_id":creator_id, "task":task, "priority":priority})
        db.session.commit()
    except:
        return False
    return True

def get_my_project_tasks(user_id, project_id):
    sql = "SELECT T.id, T.task, T.priority, T.made_at, U.username FROM project_tasks AS T," \
           " users AS U WHERE T.project_id = :project_id AND T.done = FALSE AND U.id = T.creator_id GROUP BY U.id, T.id"
    result = db.session.execute(sql, {"project_id":project_id}).fetchall()
    return result

def get_my_projects(user_id):
    sql = "SELECT P.project, P.made_at, P.id FROM projects AS P, project_members AS M " \
            " WHERE M.user_id = :user_id AND M.project_id = P.id AND P.done = FALSE"
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return result

def get_project_info(id):
    sql = "SELECT * FROM projects WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def get_project_task_info(id):
    sql = "SELECT T.id, T.task, T.priority, T.made_at, U.username FROM project_tasks AS T," \
           " users AS U WHERE T.id = :id AND T.done = FALSE AND U.id = T.creator_id GROUP BY U.id, T.id"
    return db.session.execute(sql, {"id":id}).fetchone()

def task_done(id, user_id, project_id):
    sql = "UPDATE project_tasks SET done = TRUE WHERE id = :id AND :user_id IN " \
        "(SELECT user_id FROM project_members WHERE user_id = :user_id AND project_id = :project_id)"
    db.session.execute(sql, {"id":id, "user_id":user_id, "project_id":project_id})
    db.session.commit()

def delete_project(user_id, project_id):
    if check_if_project_creator(user_id, project_id) == False:
        return False
    sql = "UPDATE projects SET done = TRUE WHERE creator_id = :user_id AND id = :project_id"
    db.session.execute(sql, {"user_id":user_id, "project_id":project_id})
    db.session.commit()
    return True

def check_if_member(project_id, user_id):
    if check_if_user_already_in_project(project_id, user_id) == False:
        abort(403)

def get_project_task_comments(project_task_id):
    sql = "SELECT C.comment, U.username, C.made_at FROM project_task_comments AS C, " \
        "users AS U WHERE project_task_id = :project_task_id AND U.id = C.creator_id ORDER BY made_at DESC"
    results = db.session.execute(sql, {"project_task_id":project_task_id}).fetchall()
    return results

def check_if_project_creator(user_id, project_id):
    sql = "SELECT id FROM projects WHERE creator_id = :user_id AND id = :project_id"
    result = db.session.execute(sql, {"user_id":user_id, "project_id":project_id}).fetchone()
    if result == None:
        return False
    else:
        return True
