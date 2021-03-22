from app import app
from flask import redirect, render_template, request, session
import users
import tasks

@app.route("/", methods=["GET","POST"])
def index():
    print(users.user_id())
    return render_template("index.html", tasks=tasks.get_my_tasks_with_comment(users.user_id()))

@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username,password):
        return redirect("/")
    else:
        return render_template("error.html",message="Invalid username or password.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/completed")
def completed():
    print("completed")
    return render_template("completed.html", tasks=tasks.get_my_completed_tasks(users.user_id()))

@app.route("/new_task", methods=["GET", "POST"])
def new_task():
    print("tultiin routes -> new task metodiin")
    users.check_csrf()
    task = request.form["new_task"]
    priority = request.form["priority"]
    print(task, priority)
    
    if tasks.new_task(users.user_id(), task, priority):
        return redirect("/")
    else:
        return render_template("error.html", message="while creating the task. Make sure it didn't exceed 50 characters or that it wasn't empty")

@app.route("/tasks/<int:id>", methods=["GET","POST"])
def task(id):
    #users.check_csrf()
    users.check_user(tasks.get_task_info(id)[1], users.user_id())
    if request.method == "GET":
        return render_template("task.html", id=id, creator_id=tasks.get_task_info(id)[1], task=tasks.get_task_info(id)[2],
        priority=tasks.get_task_info(id)[3], time=tasks.get_task_info(id)[4], done=tasks.get_task_info(id)[5], comment=tasks.get_comment(id))

    if request.method == "POST":
        print("tuli post metodilla")
        #Checks whether the user pressed 'Comment' or 'Task Done'
        try:
            print("kokeilee")
            comment = request.form["new_comment"]
            print(comment)
            print(id)
            if tasks.new_comment(users.user_id(), id, comment):
                return redirect("/")
            else: return render_template("error.html", message="Comments can't exceed 500 characters.")
        except:
            print("meni exceptiin")
            tasks.task_done(id, users.user_id())
            return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Make sure your username did not exceed 20 characters.")
    