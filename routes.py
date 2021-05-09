from app import app
from flask import redirect, render_template, request, session, url_for
import users, tasks, proj
from forms import RegisterForm, LoginForm, TaskForm, TaskComment, ProjectForm, InviteForm

@app.route("/", methods=["GET","POST"])
def index():
    form = LoginForm()
    task_form = TaskForm()
    return render_template("index.html", tasks=tasks.get_my_tasks_with_comment(users.user_id()),
                             form = form, task_form = task_form)

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
        priority=tasks.get_task_info(id)[3], time=tasks.get_task_info(id)[4], done=tasks.get_task_info(id)[5],
        comment=tasks.get_comment(id), form = form)

    if request.method == "POST":
        done = request.form["done"]
        if done == "no":
            if form.validate_on_submit():
                comment = form.comment.data
                if tasks.new_comment(users.user_id(), id, comment):
                    return redirect("/")
                else: return render_template("error.html", message="There was an error while commenting")
            return render_template("task.html", id=id, creator_id=tasks.get_task_info(id)[1],
                                    task=tasks.get_task_info(id)[2], priority=tasks.get_task_info(id)[3],
                                    time=tasks.get_task_info(id)[4], done=tasks.get_task_info(id)[5],
                                    comment=tasks.get_comment(id), form = form)
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

@app.route("/projects", methods=["GET", "POST"])
def projects():
    form = ProjectForm()

    return render_template("projects.html", form=form, projects = proj.get_my_projects(users.user_id()))

@app.route("/new_project", methods=["GET", "POST"])
def new_project():
    form = ProjectForm(request.form)
    invite_form = InviteForm()
    if form.validate_on_submit():
        project = form.project.data
        if proj.new_project(users.user_id(), project):
            return redirect("/projects")
        else:
            return render_template("error.html", message="Project creation failed")
    return render_template("projects.html", form=form, projects = proj.get_my_projects(users.user_id()))

@app.route("/projects/<int:id>", methods=["GET", "POST"])
def project(id):
    form = TaskForm()
    invite_form = InviteForm()
    proj.check_if_member(id, users.user_id())
    tasks = proj.get_my_project_tasks(users.user_id(), id)
    members = proj.get_project_members(id)
    if request.method == "GET":
        return render_template("project.html", project = proj.get_project_info(id), form = form,
                                invite_form = invite_form, tasks = tasks, id = id, members = members)
    if request.method == "POST":
        if invite_form.validate_on_submit():
            username = invite_form.username.data
            invite_id = users.get_user_id_from_username(username)
            if invite_id != None:
                proj.new_project_member(id, invite_id)
                return redirect(str(id))
            else:
                return render_template("project.html", project = proj.get_project_info(id), form = form,
                                invite_form = invite_form, tasks = tasks, id = id, members = members,
                                error = "User does not exist")

        return render_template("project.html", project = proj.get_project_info(id), form = form,
                                invite_form = invite_form, tasks = tasks, id = id, members = members)

@app.route("/projects/<int:project_id>/<int:id>", methods={"GET","POST"})
def project_task(project_id, id):
    form = TaskComment()
    proj.check_if_member(project_id, users.user_id())
    project_name = proj.get_project_info(project_id)[2]
    task = proj.get_project_task_info(id)
    comments = proj.get_project_task_comments(id)
    if request.method == "GET":
        return render_template("project_task.html", task = task, project_id = project_id, id = id,
                                 form = form, project_name = project_name, comments = comments)
    if request.method == "POST":
        done = request.form["done"]
        if done == "no":
            if form.validate_on_submit():
                comment = form.comment.data
                if proj.new_project_task_comment(users.user_id(), id, comment):
                    return redirect("/projects/" + str(project_id) + "/" + str(id))
                else: return render_template("error.html", message="There was an error while commenting")
            return render_template("project_task.html", task = task, project_id = project_id, id = id,
                                     form = form, project_name = project_name, comments = comments)
        else:
            proj.task_done(id, users.user_id(), project_id)
            return redirect("/projects/" + str(project_id))

@app.route("/new_project_task", methods=["GET", "POST"])
def new_project_task():
    form = TaskForm(request.form)
    id = request.form["id"]
    if request.method == "POST":
        try:
            done = request.form["done"]
            if proj.delete_project(users.user_id(), id) == False:
                return render_template("error.html", message="Invalid rights!")
            return redirect("/projects")
        except:
            if form.validate_on_submit():
                task = form.task.data
                priority = form.priority.data
                if proj.new_project_task(id, users.user_id(), task, priority):
                    return redirect("/projects/"+id)
                else:
                    return render_template("error.html", message="There was an error while creating a project task")
        
    return render_template("project.html", project = proj.get_project_info(id), form = form)
