#I had to name this 'proj' because the functions wouldn't
#work if it was named 'projects'...
from db import db
from flask import session, abort
import users

def new_project(creator_id, project):
    if len(project) < 3: return False
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
    #I should probably just add a column for usernames in the project_members table
    sql = "SELECT user_id FROM project_members WHERE project_id = :project_id"
    results = db.session.execute(sql, {"project_id":project_id}).fetchall()
    member_usernames = []
    for member in results:
        member_usernames.append(users.get_username_from_id(member[0]))
    return member_usernames

def new_project_task_comment(creator_id, task_id, comment):
    if len(comment) > 500:return False
    creator_username = users.get_username_from_id(creator_id)
    try:
        sql = "INSERT INTO project_task_comments (project_task_id, creator_id, comment, made_at, visible, creator_username) " \
              " VALUES (:project_task_id, :creator_id, :comment, NOW(), TRUE, :creator_username)"
        db.session.execute(sql, {"project_task_id":task_id, "creator_id":creator_id, "comment":comment, "creator_username":creator_username})
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

        hae_sql_task_id = "SELECT id FROM project_tasks WHERE project_id = :project_id AND " \
            " creator_id = :creator_id ORDER BY id DESC"
        task_id = db.session.execute(hae_sql_task_id, {"project_id":project_id, "creator_id":creator_id}).fetchone()
        cretor_username = users.get_username_from_id(creator_id)
        new_project_task_comment(creator_id, task_id[0], "Click to set a comment")

    except:
        return False
    return True

def get_my_project_tasks(user_id, project_id):
    ###
    sql = "SELECT T.id, T.task, T.priority, T.made_at, C.comment FROM project_tasks AS T," \
           " project_task_comments AS C WHERE T.project_id = :project_id AND C.project_task_id = T.id AND T.done = FALSE GROUP BY T.id, C.comment"
    sql2 = "SELECT T.id, T.task, T.priority, T.made_at FROM project_tasks AS T," \
           " project_task_comments AS C WHERE T.project_id = :project_id AND T.done = FALSE GROUP BY T.id"
    result = db.session.execute(sql2, {"project_id":project_id}).fetchall()
    return result

def get_my_projects(user_id):
    sql = "SELECT P.project, P.made_at, P.id FROM projects AS P, project_members AS M " \
            " WHERE M.user_id = :user_id AND M.project_id = P.id AND P.done = FALSE"
    ##
    sql2 = "SELECT P.project, P.made_at, P.id, COUNT(M.id) FROM projects AS P, " \
            " project_members AS M WHERE M.user_id = :user_id AND M.project_id = P.id AND P.done = FALSE GROUP BY M.id"
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return result

def get_project_info(id):
    sql = "SELECT * FROM projects WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def get_project_task_info(id):
    sql = "SELECT T.id, T.task, T.priority, T.made_at, C.comment FROM project_tasks as T, " \
        "project_task_comments AS C WHERE T.id = :id ORDER BY C.id DESC"
    return db.session.execute(sql, {"id":id}).fetchone()
#tähän pitää lisätä oikeudet kaikille jotka kuuluu projektiin
def task_done(id, user_id):
    sql = "UPDATE project_tasks SET done=TRUE WHERE id=:id AND creator_id = :user_id"
    db.session.execute(sql, {"id":id, "user_id":user_id})
    db.session.commit()

def delete_project(user_id, project_id):
    ###! confirmaa
    sql = "UPDATE projects SET done = TRUE WHERE creator_id = :user_id AND id = :project_id"
    db.session.execute(sql, {"user_id":user_id, "project_id":project_id})
    db.session.commit()

def check_if_member(project_id, user_id):
    if check_if_user_already_in_project(project_id, user_id) == False:
        abort(403)

def get_project_task_comments(project_task_id):
    sql = "SELECT comment, creator_username, made_at FROM project_task_comments WHERE project_task_id = :project_task_id ORDER BY made_at DESC"
    results = db.session.execute(sql, {"project_task_id":project_task_id}).fetchall()
    
    return results

