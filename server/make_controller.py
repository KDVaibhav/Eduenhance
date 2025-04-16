import sys
import os
if len(sys.argv) < 2:
    print("Please provide controller name.")
    exit(-1)
if len(sys.argv) < 3:
    print("Please provide controller type (1 for CRUD, 2 for RU).")
    exit(-1)
controller_name = sys.argv[1]
controller_type = sys.argv[2]
os.mkdir(os.getcwd() + '/een/web/blueprints/' + controller_name.lower())

if controller_type == '1':
    file_paths = [
        "een/web/blueprints/"+controller_name.lower()+"/__init__.py",
        "een/web/blueprints/"+controller_name.lower()+"/controller.py",
        "een/web/blueprints/"+controller_name.lower()+"/"+controller_name.lower()+"_form.html",
        "een/web/blueprints/"+controller_name.lower()+"/"+controller_name.lower()+".py"
    ]

    file_codes = []
    file_codes.append("""from ."""+controller_name.lower()+""" import """+controller_name.lower())
    file_codes.append("""from een.db import """+controller_name.lower()+"""
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool


class """+controller_name+"""Controller(CrudController):
    def __init__(self):
        \"\"\"Initializes new instance of the """+controller_name+"""Controller class\"\"\"
        super().__init__("""+controller_name.lower()+"""(getSchool()), namespace=\""""+controller_name.lower()+"""\", columns=[\"name\"])

    def _update_model(self, model, data, files):
        model.name = data.get("name", None)
""")
    file_codes.append("""{% macro form(model, action='', allow_edit=true) -%}
    <form action="{{ action }}" method="post" class="form-horizontal">
        <!-- Name -->
        <div class="form-group">
            <label class="col-sm-2 control-label">Name</label>
            <div class="col-sm-10">
                <input
                    name="name"
                    class="form-control input-lg"
                    placeholder="Name"
                    value="{{ model.name }}"
                    autocomplete="off"
                    {%if not allow_edit%}readonly{%endif%}
                >
            </div>
        </div>

        <!-- Submit -->
        {%if allow_edit%}
        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
                <input id="submit"
                    type="submit"
                    class="form-control btn btn-primary"
                >
            </div>
        </div>
        {%endif%}
    </form>
{%- endmacro %}""")
    file_codes.append("""from flask import Blueprint, request

from .controller import """+controller_name+"""Controller

"""+controller_name.lower()+""" = Blueprint(\""""+controller_name.lower()+"""\", __name__, template_folder=".")


@"""+controller_name.lower()+""".route("/")
def index():
    controller = """+controller_name+"""Controller()
    return controller.index()


@"""+controller_name.lower()+""".route("/new", methods=["GET", "POST"])
def create():
    controller = """+controller_name+"""Controller()
    return controller.create(request)


@"""+controller_name.lower()+""".route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = """+controller_name+"""Controller()
    return controller.update(request, key)
""")

elif controller_type == '2':
    file_paths = [
        "een/web/blueprints/"+controller_name.lower()+"/__init__.py",
        "een/web/blueprints/"+controller_name.lower()+"/controller.py",
        "een/web/blueprints/"+controller_name.lower()+"/"+controller_name.lower()+"_view.html",
        "een/web/blueprints/"+controller_name.lower()+"/"+controller_name.lower()+".py"
    ]

    file_codes = []
    file_codes.append("""from ."""+controller_name.lower()+""" import """+controller_name.lower())
    file_codes.append("""from flask import render_template, flash, redirect
from flask_login.utils import login_required, current_user
import json

from een.db import """+controller_name.lower()+""", classes
from een.web.app.auth import access_denied, has_permission
from localstorage import getSchool


class """+controller_name+"""Controller():
    def __init__(self):
        \"\"\"Initializes new instance of the """+controller_name+""" Controller class\"\"\"
        self._repository = """+controller_name.lower()+"""(getSchool())
        self._namespace = \""""+controller_name.lower()+"""\"
        self._model_name = \""""+controller_name.lower()+"""\"
        self._permission = \""""+controller_name.lower()+"""\"
        self._html = \""""+controller_name.lower()+"""_view.html\"
        self._url = \""""+controller_name.lower()+"""\"

    @login_required
    def index(self):
        if (not has_permission(\""""+controller_name.lower()+""".read_all\")) and (not has_permission(\""""+controller_name.lower()+""".read_own\")) and (not has_permission(\""""+controller_name.lower()+""".update\")):
            return access_denied()
        models = self._repository.all()
        for i in range(len(models)):
            del models[i]['_id']
        params = {}
        if has_permission(\""""+controller_name.lower()+""".read_all\"):
            params['models'] = json.dumps(models)
        if has_permission(\""""+controller_name.lower()+""".read_own\"):
            params['model_class'] = models[current_user.class_]
            params['model_class_js'] = json.dumps(params['model_class'])
        return render_template("crud/index_special.html", **params, **self.__options(), **self._extend(None))

    @login_required
    def update(self, request):
        \"\"\"Shows """+controller_name.lower()+""".\"\"\"
        if request.method == "POST":
            if has_permission(\""""+controller_name.lower()+""".update\"):
                class_ = request.form.get("class", "")
                d = self._repository.find_one({"class_": class_})
                if not d:
                    self._repository.insert({"class_": class_})
                else:
                    self._repository.save(d)

                flash("{} was successfully updated".format(self._model_name), category="success")
                return redirect("/" + self._url)
            else:
                return access_denied()

    def _extend(self, model):
        return {
            "classes": list(map(lambda x: x.name, sorted(classes(getSchool()).all(), key = lambda x: x.name)))
        }

    def __options(self):
        return {
            "index": self._html,
            "active_page": self._namespace,
            "url": self._url,
            "model_name": self._model_name,
            "namespace": self._namespace,
            "allow_edit": has_permission(\""""+controller_name.lower()+""".update\"),
            "allow_view": has_permission(\""""+controller_name.lower()+""".read_all\")
        }
""")
    file_codes.append("""{% macro index(action='', allow_edit=true) -%}
{%if allow_edit%}
    <div class=\""""+controller_name.lower()+"""-container\">
        <h4>Edit """+controller_name+"""</h4>    
        <form action="{{ action }}" method="post">
            <select id="classes-edit" name="class">
                <option value="">Select a class</option>
                {%for class in classes%}
                    <option>{{class}}</option>
                {%endfor%}
            </select>
            <button type="button" onclick="show_edit()">Show</button>

            <input type="submit" value="Submit" disabled id="submit_button">
        </form>
    </div>
    <script>
        function show_edit() {
            var e = document.getElementById("classes-edit")
            var class_ = e.options[e.selectedIndex].value
            if (!class_) {
                alert("Class is not selected.")
                return
            }
            $("#submit_button").removeAttr("disabled")
        }
    </script>
{%endif%}



{%if allow_view%}
    <div class=\""""+controller_name.lower()+"""-containe.lower()r\">
        <h4>View """+controller_name+"""</h4>    
        <select id="classes-view" name="class">
            <option value="">Select a class</option>
            {%for class in classes%}
                <option>{{class}}</option>
            {%endfor%}
        </select>
        <button type="button" onclick="show_view()">Show</button>
    </div>
    <script>
        function show_view() {
            var e = document.getElementById("classes-view")
            var class_ = e.options[e.selectedIndex].value
            if (!class_) {
                alert("Class is not selected.")
                return
            }
        }
    </script>
{%endif%}
{%if model_class%}
    <div class=\""""+controller_name.lower()+"""-container\">
        <h4>Your """+controller_name+"""</h4>
    </div>
{%endif%}
<style>
    ."""+controller_name.lower()+"""-container {
        margin: 40px;
    }
</style>
<script>
</script>
{%endmacro%}
""")
    file_codes.append("""from flask import Blueprint, request

from .controller import """+controller_name+"""Controller

"""+controller_name.lower()+""" = Blueprint(\""""+controller_name.lower()+"""\", __name__, template_folder=".")


@"""+controller_name.lower()+""".route("/", methods=["GET", "POST"])
def index():
    controller = """+controller_name+"""Controller()
    if request.method == "GET": 
        return controller.index()
    if request.method == "POST": 
        return controller.update(request)

""")


for i in range(4):
    with open(file_paths[i], "w") as controller_file:
        controller_file.write(file_codes[i])

print("Remember to change::\n|| Roles controller (een/web/blueprints/roles/controller.py) ||\n|| Navigation bar (een/web/templates/general.html) ||\n|| App file (app.py) ||")