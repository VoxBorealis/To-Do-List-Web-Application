from app import app
from flask import redirect, render_template, request, session
import users
import tasks
from forms import RegisterForm, LoginForm, TaskForm, TaskComment

@app.route("/", methods=["GET","POST"])
def index():
    form = LoginForm()
    task_form = TaskForm()
    return render_template("index.html", tasks=tasks.get_my_tasks_with_comment(users.user_id()), form = form, task_form = task_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("index.html",form = form, error ="Invalid username or password")
            #return render_template("error.html",message="Invalid username or password.")
    return render_template("index.html", form = form)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/completed")
def completed():
    return render_template("completed.html", tasks=tasks.get_my_completed_tasks(users.user_id()))

@app.route("/new_task", methods=["GET", "POST"])
def new_task():
    form = TaskForm(request.form)
    if form.validate_on_submit():
        task = form.task.data
        priority = form.priority.data
        if (tasks.new_task(users.user_id(), task, priority)):
            return redirect("/")
        else:
            return render_template("error.html",message="There was an error while creating a task")
    return render_template("index.html", tasks=tasks.get_my_tasks_with_comment(users.user_id()), task_form = form)

@app.route("/tasks/<int:id>", methods=["GET","POST"])
def task(id):
    form = TaskComment()
    users.check_user(tasks.get_task_info(id)[1], users.user_id())
    if request.method == "GET":
        return render_template("task.html", id=id, creator_id=tasks.get_task_info(id)[1], task=tasks.get_task_info(id)[2],
        priority=tasks.get_task_info(id)[3], time=tasks.get_task_info(id)[4], done=tasks.get_task_info(id)[5], comment=tasks.get_comment(id), form = form)

    if request.method == "POST":
        done = request.form["done"]
        if done == "no":
            if form.validate_on_submit():
                comment = form.comment.data
                if tasks.new_comment(users.user_id(), id, comment):
                    return redirect("/")
                else: return render_template("error.html", message="There was an error while commenting")
            return render_template("task.html", id=id, creator_id=tasks.get_task_info(id)[1], task=tasks.get_task_info(id)[2],
            priority=tasks.get_task_info(id)[3], time=tasks.get_task_info(id)[4], done=tasks.get_task_info(id)[5], comment=tasks.get_comment(id), form = form)
        else:
            tasks.task_done(id, users.user_id())
            return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Account creation failed")
    return render_template("register.html", form=form)
    