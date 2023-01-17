from application import app, todo
from flask import render_template, request, url_for, flash, redirect
from .forms import TodoForm
from datetime import datetime
import pymongo
from bson import ObjectId

@app.route("/")
def home_page():
    todos = []
    for item in todo.find().sort("date_created", pymongo.ASCENDING):
        item["_id"] = str(item["_id"])
        item["date_created"] = item["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(item)
    return render_template("view_todos.html", title="View", todos=todos)

@app.route("/add_todo", methods=["GET", "POST"])
def add_todo_page():
    if request.method == "POST":
        form = TodoForm(request.form)
        name = form.name.data
        description = form.description.data
        completed = form.completed.data

        todo.insert_one({
            "name": name,
            "description": description,
            "completed": completed,
            "date_created": datetime.utcnow()
        })

        flash("Todo added successfully!", "success")
        return redirect(url_for("home_page"))
    else:
        form = TodoForm()
    return render_template("add_todo.html", form=form)


@app.route("/update_todo/<_id>", methods=["POST", "GET"])
def update_todo_page(_id):
    if request.method == "POST":
        form = TodoForm(request.form)
        name = form.name.data
        description = form.description.data
        completed = form.completed.data

        todo.find_one_and_update({"_id": ObjectId(_id)}, { "$set":
        {
            "name": name,
            "description": description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }})
        flash("Todo updated successfully", "success")
        return redirect(url_for("home_page"))
    else:
        if len(_id) == 24:
            todo_item = todo.find_one({"_id": ObjectId(_id)}) 
            if todo_item:
                form  = TodoForm()
                # fill form with todo_item (like placeholder)
                form.name.data = todo_item.get("name", None)
                form.description.data = todo_item.get("description", None)
                form.completed.data = todo_item.get("completed", None)
                return render_template("update_todo.html", form=form)

        flash("Todo item not found", "warning")
        return redirect(url_for("home_page"))


@app.route("/delete/<_id>", methods=["POST", "GET"])
def delete_todo_page(_id):
    todo.find_one_and_delete({"_id": ObjectId(_id)})
    flash("Todo item deleted successfully", "success")
    return redirect(url_for("home_page"))