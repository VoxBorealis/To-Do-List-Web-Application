from app import app
from flask import redirect, render_template, request, session
import users
import tasks

@app.route("/", methods=["GET","POST"])
def index():
    print(users.user_id())
    return render_template("index.html", tasks=tasks.get_my_tasks(users.user_id()))

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

@app.route("/done")
def done():
    print("done!")

@app.route("/new_task", methods=["GET", "POST"])
def new_task():
    print("tultiin routes -> new task metodiin")
    task = request.form["new_task"]
    priority = request.form["priority"]
    print(task, priority)
    tasks.new_task(users.user_id(), task, priority)
    return redirect("/")

#@app.route("/new_comment", methods=["GET", "POST"])
#def new_comment():
#    print("Tultiin routes -> new_comment metodiin")
#    comment = request.form["new_comment"]
#    print(comment)
#    task_id = request.data["id"]
#    print(task_id)
    
#   tasks.new_comment(users.user_id(), task_id, comment)

@app.route("/tasks/<int:id>", methods=["GET","POST"])
def task(id):
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
            tasks.new_comment(users.user_id(), id, comment)
            return redirect("/")
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
            return render_template("error.html", message="There was an error while creating your account.")
    