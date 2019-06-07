import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  # to convert the ID to a format readable by MongoDB


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template('tasks.html', 
                           tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
                           categories=mongo.db.categories.find())


@app.route('/insert_task', methods=['POST',])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict()) # in a real case you would add some validation
    return redirect(url_for('get_tasks'))

    
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    print('task_id', task_id, ObjectId(task_id))
    the_task = mongo.db.task.find_one({'_id': ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    print("the_task", the_task)
    print("all_categories", all_categories)
    return render_template('edittask.html',
                           task=the_task,
                           categories=all_categories,)
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)